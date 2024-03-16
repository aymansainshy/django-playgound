from rest_framework import serializers
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
