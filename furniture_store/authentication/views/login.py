from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers.login import LoginSerializer
from rest_framework.permissions import AllowAny

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
