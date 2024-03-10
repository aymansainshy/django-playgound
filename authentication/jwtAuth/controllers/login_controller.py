from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from ..serializers import UserSerializer, LoginSerializer


def login(request) -> Response:
    # serializer act as validator middleware
    loginSerializer = LoginSerializer(data=request.data)

    if loginSerializer.is_valid(raise_exception=True):
        email = request.data['email']
        password = request.data['password']

        # Find the user by email in database
        user: User = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed("Wrong password!")
            # return Response(
            #     data={
            #         'code': '0',
            #         'error': 'Wrong password',
            #         'status': status.HTTP_400_BAD_REQUEST
            #     },
            #     status=status.HTTP_400_BAD_REQUEST
            # )
        # else return the founded user
        accessToken = RefreshToken.for_user(user)
        userSerializer = UserSerializer(user)
        return Response({
            'data': userSerializer.data,
            'access_token': str(accessToken),
        })

    # return Response(loginSerializer.errors, status=status.HTTP_404_NOT_FOUND)
