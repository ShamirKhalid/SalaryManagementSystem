# security_access_control/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from authentication.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_active', 'is_staff', 'groups', 'user_permissions')
