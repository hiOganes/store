from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.serializers import RegisterSerialier
from apps.accounts.models import User
from apps.accounts import schema_examples


@extend_schema(**schema_examples.registers_schema)
class RegisterAPIView(APIView):
    serializer_class = RegisterSerialier
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.model(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({'group': 'users'})
            auth_keys = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data=auth_keys, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(**schema_examples.custom_token_obtain_pair_schema)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(**schema_examples.custom_token_refresh_schema)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(**schema_examples.custom_token_verify_schema)
class CustomTokenVerifyView(TokenVerifyView):
    pass