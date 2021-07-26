from django.urls import reverse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_response(self, request, response):
        if not request.user.is_authenticated:
            if request.path not in [reverse('create-account'), reverse('password_reset')] and 'admin' not in request.path:
                if request.path != reverse('login'):
                    return redirect(reverse('login'))
        return response
