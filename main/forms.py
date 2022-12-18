from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from .models import Talk, User

class LoginForm(AuthenticationForm):
    pass

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}
        help_texts = {"email": ""}