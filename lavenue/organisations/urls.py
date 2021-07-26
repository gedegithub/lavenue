from django.urls import path

from organisations.views import CreateMeetingView, CreateOrganisationView, OrganisationHomepageView, AgendaView

urlpatterns = [
    path('create-organisation/', CreateOrganisationView.as_view(), name='create-organisation'),
    path('<slug:organisation_slug>/', OrganisationHomepageView.as_view(), name='organisation-homepage'),
    path('<slug:organisation_slug>/create-meeting/', CreateMeetingView.as_view(), name='create-meeting'),
    path('<slug:organisation_slug>/<slug:meeting_slug>/agenda/', AgendaView.as_view(), name='meeting-agenda'),
]

app_name = 'organisations'