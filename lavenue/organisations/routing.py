from django.urls import path

from organisations.consumers.meeting_consumer import MeetingConsumer

websocket_urlpatterns = [
    path('ws/meeting/<slug:meeting_slug>/', MeetingConsumer.as_asgi())
]