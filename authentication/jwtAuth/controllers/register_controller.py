from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from ..serializers import RegisterSerializer, UserResponseSerializer


def register(request):
    user_serializer = RegisterSerializer(data=request.data)

    if user_serializer.is_valid(raise_exception=True):
        savedUser = user_serializer.save()
        accessToken = AccessToken.for_user(savedUser)

        user_serializer = UserResponseSerializer(savedUser)
        return Response({
            'data': user_serializer.data,
            'access_token': str(accessToken),
            'pyload': accessToken.payload,
        })

    # return Response(userSerializer.errors, status=status.HTTP_404_NOT_FOUND)
