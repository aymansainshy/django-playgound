from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from jwtAuth.models import User
from jwtAuth.serializers import UserSerializer


def login(request):
    email = request.data['email']
    password = request.data['password']

    # Find the user by email in database
    user = User.objects.filter(email=email).first()

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
    accessToken = AccessToken.for_user(user)
    userSerializer = UserSerializer(user)
    return Response({
        'data': userSerializer.data,
        'access_token': str(accessToken),
    })
