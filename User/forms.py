from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password'}
    ))


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'john.doe@example.com', 'type': 'email', 'name': 'email',
               'id': 'email', }))


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'new_password1'}
    ))

    new_password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'new_password2'}
    ))
