from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from core.settings import SECRET_KEY
import jwt
from rest_framework import generics, status, views
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib import auth

from .serializers import (EmailVerificationSerializer, RegisterSerializer, LoginSerializer)
from .utils import Utils


# class RegisterView(generics.GenericAPIView):
#     userSerializer = UserResponseSerializer
#
#     def post(self, request):
#         return register_controller.register(self.request)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        # email_verification_serializer = self.serializer_class(data=request.GET.get('token'))
        #
        # if email_verification_serializer.is_valid(raise_exception=True):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as error:
            return Response({'error': f'Invalid token {error}'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            raise


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)

        if user_serializer.is_valid(raise_exception=True):
            saved_user = user_serializer.save()

            # This will get the domain name for this server
            current_site = get_current_site(request).domain
            # Internal route for verifying email
            relative_link = reverse('email-verify')
            # Generated link below as email body
            abs_url = 'http://' + current_site + relative_link + '?token=' + str(user_serializer.data['access_token'])
            email_body = 'Hi ' + saved_user.username + ' use link below to verify your email \n' + abs_url
            data = {
                'email_body': email_body,
                'to_email': saved_user.email,
                'email_subject': 'Verify Your email address'
            }
            # Sending email for verifications
            Utils.send_email(data)

            return Response(
                data=user_serializer.data,
                status=status.HTTP_201_CREATED
            )

        # return Response(userSerializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login(request):
    # serializer act as validator middleware
    user_serializer = LoginSerializer(data=request.data)

    if user_serializer.is_valid(raise_exception=True):
        email = request.data['email']
        password = request.data['password']

        # Find the user by email in database
        # user: User = User.objects.filter(email=email).first()
        # if not user.check_password(password):
        #     raise AuthenticationFailed("Wrong password!")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, please try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email not verified')

        # return Response(
        #     data={
        #         'code': '0',
        #         'error': 'Wrong password',
        #         'status': status.HTTP_400_BAD_REQUEST
        #     },
        #     status=status.HTTP_400_BAD_REQUEST
        # )
        # else return the founded user
        user_serializer = LoginSerializer(user)
        return Response(
            data=user_serializer.data,
            status=status.HTTP_200_OK
        )

    # return Response(loginSerializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def testToken(request):
    return Response({"passed!"})
