from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# You can extend TokenObtainPairView if you want custom claims or behavior.
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens.
    You can override methods here to customize the token claims.
    """
    pass