# chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Optionally customize JWT authentication logic.
    Still uses standard JWT behavior.
    """
    def authenticate(self, request):
        # You can add logging or other behavior here
        return super().authenticate(request)
