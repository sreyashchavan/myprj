from django import forms
from .models import Comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxLengthValidator

class CommentForm(forms.ModelForm):
    class Meta():
        model= Comments
        exclude=["post"]
        labels={
            "user_name": "Your name",
            "text": "Comment"
        }

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = Register
#         fields="__all__"
#         labels={
#             "user_name":"Username",
#             "email_id":"Email",
#             "password_1":"Password",
#             "password_2":"Confirm Password"
#         }
#         widgets = {
#             'password_1': forms.PasswordInput(),
#             'password_2': forms.PasswordInput(),
#         }

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8),MaxLengthValidator(8)]  # Minimum length of 8 characters
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8),MaxLengthValidator(8)]  # Minimum length of 8 characters
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
