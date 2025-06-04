from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed

class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_X_CUSTOM_TOKEN')
        if not token:
            return None  # No token, let other authenticators try

        # Example: Fake lookup just for demonstration
        if token == "secret-token":
            from django.contrib.auth import get_user_model
            user = get_user_model().objects.first()  # simulate a lookup
            return (user, None)
        raise AuthenticationFailed("Invalid custom token")
