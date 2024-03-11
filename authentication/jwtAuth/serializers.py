from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # fields = '__all__'

        # To hide password and don't return it in response
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError('The username must only contain characters')
        return super().validate(attrs)

    def create(self, validated_data) -> User:
        return User.objects.createUser(**validated_data)

    # def create(self, validated_data) -> User:
    #     password = validated_data.pop('password', None)
    #     user = self.Meta.model(**validated_data)
    #     if password is not None:
    #         user.set_password(password)
    #     user.save()
    #     return user


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'password']
        fields = '__all__'

        # To hide password and don't return it in response
        extra_kwargs = {
            "password": {"write_only": True}
        }
