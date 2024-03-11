from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from ..models import User
from ..serializers import RegisterSerializer, UserResponseSerializer
from ..utils import Utils


def register(request):
    user_serializer = RegisterSerializer(data=request.data)

    if user_serializer.is_valid(raise_exception=True):
        saved_user = user_serializer.save()
        token = AccessToken.for_user(saved_user)

        # Sending email for verifications
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = 'https://' + current_site + relative_link + '?token=' + str(token)
        email_body = 'Hi ' + saved_user.username + 'use link below to verify your email \n' + abs_url
        data = {
            'email_body': email_body,
            'to_email': saved_user.email,
            'email_subject': 'Verify Your email address'
        }
        Utils.sendEmail(data)

        user_serializer = UserResponseSerializer(saved_user)
        return Response({
            'data': user_serializer.data,
            'access_token': str(token),
            'pyload': token.payload,
        })

    # return Response(userSerializer.errors, status=status.HTTP_404_NOT_FOUND)
