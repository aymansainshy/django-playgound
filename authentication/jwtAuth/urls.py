from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login),
    path('varify-token', views.test_token),
]
