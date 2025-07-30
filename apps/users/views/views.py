from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.users.serializers.serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from apps.users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
