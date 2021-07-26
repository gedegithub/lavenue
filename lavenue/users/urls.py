from django.urls import path

from users.views import CreateAccountView

urlpatterns = [
    path('create/', CreateAccountView.as_view(), name='create-account'),
]
