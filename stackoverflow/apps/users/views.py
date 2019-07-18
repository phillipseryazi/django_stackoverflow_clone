from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from .renderers import UserRenderer
from .models import User
from .serializers import (RegistrationSerializer, LoginSerializer, ProfileSerializer)
from .backends import JWTAuthentication
from ...utils.decoder import decode_token
from ...utils.emailer import send_email


# Create your views here.


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (UserRenderer,)

    def get(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        try:
            user = User.objects.get(id=token_data['id'])
        except User.DoesNotExist:
            return Response({'details': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=self.serializer_class(user).data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        pass
