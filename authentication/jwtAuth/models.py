from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class UserManager(BaseUserManager):
    def createUser(self, email, username=None, password=None):
        # if username is None:
        #     raise TypeError("username is required")
        if email is None:
            raise TypeError("email is required")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def createSuperUser(self, username, email, password):
        if password is None:
            raise TypeError("password is required")
        user = self.createUser(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # To tell Django how to manage objects of this type User
    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        token = AccessToken.for_user(self)
        return str(token)
