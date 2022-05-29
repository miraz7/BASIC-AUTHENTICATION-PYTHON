from os import name
from django.contrib import admin
from django.urls import path, include

from user.views import RegistrationVerificationCodeView, RegsiterUserView, UserLoginView

urlpatterns=[
    path('register/',RegsiterUserView.as_view(), name="register_user" ),
    path('registration-verification/', RegistrationVerificationCodeView.as_view(), name='confirm_validation_code'),
    path('login/', UserLoginView.as_view(), name='user_login'),

]