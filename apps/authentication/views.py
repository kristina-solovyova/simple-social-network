from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import UserSerializer, JWTSerializer


class UserLogin(ObtainJSONWebToken):
    permission_classes = (AllowAny,)
    serializer_class = JWTSerializer


class UserRegistration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
