from rest_framework import generics
from authentication.serializers.register import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
