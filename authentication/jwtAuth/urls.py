from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.login, name='login'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-password', views.RequestPasswordResetEmail.as_view(), name='request-reset-password'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('set-new-password', views.SetNewPasswordAPIView.as_view(), name='set-new-password'),

    path('test-token', views.testToken, name='verify-token'),
]
