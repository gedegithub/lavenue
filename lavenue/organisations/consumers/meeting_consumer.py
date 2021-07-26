import json
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from speakers.forms import InterventionForm, MotionForm
from speakers.models import Participant
from organisations.models import Meeting, MemberRequests
from motions.models import Ballot, Motion, Vote
from organisations.mappings import member_request_mapping


class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.meeting_slug = self.scope['url_route']['kwargs']['meeting_slug']
        self.meeting_group_slug = self.meeting_slug
        await self.channel_layer.group_add(
            self.meeting_group_slug,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.meeting_group_slug,
            self.channel_name
        )
    
    @sync_to_async
    def create_motion(self, text_data_json, payload):
        motion = MotionForm(text_data_json.get('motion_form'))
        if motion.is_valid():
            motion.save()
            payload['form_type'] = 'motion-form'
        else:
            payload['form_error'] = True

    @sync_to_async
    def create_intervention(self, text_data_json, payload):
        intervention = InterventionForm(text_data_json.get('intervention_form'))
        if intervention.is_valid():
            intervention.save()
            payload['form_type'] = 'intervention-form'
        else:
            payload['form_error'] = True

    @sync_to_async
    def store_joinees(self, text_data_json, payload):
        payload['action'] = 'joining'
        payload['participant_name'] = text_data_json.get('participant_name')
        meeting = Meeting.objects.filter(slug=text_data_json.get('meeting_slug')).first()
        joinees = list(meeting.joinees)
        joinees.append(payload['participant_name'])
        joinees = set(joinees)
        joinees = list(joinees)
        Meeting.objects.filter(slug=text_data_json.get('meeting_slug')).update(joinees=joinees)
        payload['joinees'] = joinees

    @sync_to_async
    def end_meet(self, text_data_json, payload):
        vote = Vote.objects.filter(motion__id=text_data_json.get('motion_id')).first()
        if vote.favour > (vote.oppose and vote.abstain):
            vote.passed = True
            vote.save()
            payload['pass_proposition'] = True
            motion = getattr(vote, 'motion')
            payload['passed_proposition_name'] = motion.get_proposition_display() + ' has passed'
        payload['action'] = 'end_meet'

    @sync_to_async
    def submit_vote(self, text_data_json, payload):

        payload['participant_id'] = text_data_json.get('participant_id')
        participant = Participant.objects.filter(user__id=text_data_json.get('participant_id')).first()
        motion = Motion.objects.filter(id=text_data_json.get('motion_id')).first()
        payload['action'] = "voted"
        
        vote = Vote.objects.filter(motion=motion).first()
        if not vote:
            vote = Vote.objects.create(
                motion=motion,
                requester=participant,
                favour=0,
                oppose=0,
                abstain=0,
                passed=False
            )
        vote_type = text_data_json.get('vote_type')
        Ballot.objects.create(
            participant=participant,
            vote=vote,
            cast=vote_type,
            worth=3
        )
        
        if vote_type == 's':
            vote.favour += 1
        elif vote_type == 'a':
            vote.abstain += 1
        else:
            vote.oppose += 1
        vote.save()
    
    @sync_to_async
    def submit_participant_action(self, text_data_json, payload):
        meeting_slug = text_data_json.get('meeting_slug')
        participant_id = text_data_json.get('participant_id')
        member_request_type = text_data_json.get('member_request_type')
        payload['member_request_type'] = member_request_type
        participant = Participant.objects.filter(user__id=participant_id).first()
        meeting = Meeting.objects.filter(slug=meeting_slug).first()
        member_request = MemberRequests.objects.create(
            participant=participant,
            meeting=meeting,
            request_type=member_request_type
        )
        participant_name = text_data_json.get('participant_name', '')
        payload['member_request_id'] = member_request.id
        payload['action'] = f'{participant_name} {member_request_mapping.get(member_request_type)}'

    
    @sync_to_async
    def president_confirmation(self, text_data_json, payload):
        member_request_id = text_data_json.get('member_request_id')
        member_request = MemberRequests.objects.filter(id=member_request_id)
        member_request.update(is_served=True)
        payload['member_request_id'] = text_data_json.get('member_request_id')
        member_request = member_request.first()
        participant_name = text_data_json.get('participant_name', '')
        payload['action'] = f'{participant_name} {member_request_mapping.get(member_request.request_type)}'

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json.get('sender')
        payload = {}
        participant_name = text_data_json.get('participant_name', '')
        member_request_type = text_data_json.get('member_request_type')
        try:
            if sender == 'secretary':
                if text_data_json.get('form_type') == 'motion':
                    await self.create_motion(text_data_json, payload)
                else:
                    await self.create_intervention(text_data_json, payload)
                payload['action'] = 'form_submission'
                payload['participant_id'] = text_data_json.get('participant_id')
            elif member_request_type == 'joining':
                await self.store_joinees(text_data_json, payload)
            elif member_request_type == 'end_meet':
                await self.end_meet(text_data_json, payload)
            elif member_request_type == 'vote':
                await self.submit_vote(text_data_json, payload)
                sender = 'president'
            elif sender == 'president':
               await self.president_confirmation(text_data_json, payload)
            elif sender == 'participant':
                await self.submit_participant_action(text_data_json, payload)

            payload['participant_name'] = participant_name
            payload['sender'] = sender
            await self.channel_layer.group_send(
                self.meeting_group_slug,
                {
                    'type': 'meeting_action',
                    **payload

                }
            )
        except Exception as e:
            print(e)

    # Receive message from room group
    async def meeting_action(self, event):
        payload = {}
        for key in event:
            payload[key] = event.get(key, '')
        # Send message to WebSocket
        await self.send(text_data=json.dumps(payload))