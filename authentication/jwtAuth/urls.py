from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.login, name='login'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('test-token', views.testToken, name='verify-token'),
]
