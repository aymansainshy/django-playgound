from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('verify-token', views.testToken),
]
