from django.contrib.sites.shortcuts import get_current_site
from drf_yasg.openapi import Response
from rest_framework import serializers, status
from django.urls import reverse

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (smart_str, force_str, smart_bytes,
                                   DjangoUnicodeDecodeError)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True,
                                     required=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    access_token = serializers.CharField(max_length=255, min_length=6, read_only=True)
    refresh_token = serializers.CharField(max_length=255, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_verified', 'access_token', 'refresh_token']

        # If you override them above no need to add rules here, like we didn't add password field
        extra_kwargs = {
            'is_staff': {"read_only": True},
            'is_active': {"read_only": True},
            'is_verified': {"read_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("username", "")

        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    access_token = serializers.CharField(max_length=255, min_length=6, read_only=True)
    refresh_token = serializers.CharField(max_length=255, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_verified', 'access_token', 'refresh_token']
        # fields = '__all__'

        # To hide password and don't return it in response
        extra_kwargs = {
            # "password": {"write_only": True},
            'is_staff': {"read_only": True},
            'is_active': {"read_only": True},
            'is_verified': {"read_only": True},
            # 'token': {"read_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")
        # is_staff = attrs.get("is_staff", "")

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain characters')
        # if not is_staff:
        #     raise serializers.ValidationError('The field must only contain characters')
        return super().validate(attrs)

    def create(self, validated_data) -> User:
        return User.objects.create_user(validated_data['email'],
                                        validated_data['username'],
                                        validated_data['password'])

    # def create(self, validated_data) -> User:
    #     password = validated_data.pop('password', None)
    #     user = self.Meta.model(**validated_data)
    #     if password is not None:
    #         user.set_password(password)
    #     user.save()
    #     return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        # model = User
        fields = ['new_password', 'token', 'uidb64']

    def validate(self, validated_data):
        try:
            password = validated_data.get('new_password', '')
            token = validated_data.get('token', '')
            uidb64 = validated_data.get('uidb64', '')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    detail='The reset link is invalid',
                    code=401
                )
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed(
                detail='The reset link is invalid',
                code=401
            )

        return super().validate(validated_data)
