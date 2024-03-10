from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from jwtAuth.serializers import UserSerializer


def register(request):
    userSerializer = UserSerializer(data=request.data)

    if userSerializer.is_valid():
        savedUser = userSerializer.save()
        accessToken = AccessToken.for_user(savedUser)

        return Response({
            'data': userSerializer.data,
            'access_token': str(accessToken),
            'pyload': accessToken.payload,
        })

    return Response(userSerializer.errors, status=status.HTTP_404_NOT_FOUND)
