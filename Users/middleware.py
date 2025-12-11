# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # L’utilisateur n’est pas connecté → OK
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Chemins autorisés même si must_change_password = True
        allowed_paths = {
            reverse('password_change'),
            # reverse('password_change_done'),
            reverse('logout'),
            reverse('login'),
        }

        # Ne pas bloquer l’accès à la page de changement de mot de passe
        if request.path in allowed_paths:
            return self.get_response(request)

        # Blocage si must_change_password = True
        if getattr(request.user, 'must_change_password', False):
            return redirect('password_change')
# 
        return self.get_response(request)
