from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=140)
    # email = forms.EmailField(max_length=140)
    password = forms.CharField(max_length=140, widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})


class CreateAccountForm(UserCreationForm):
    """ """
    # self.username.widget.attrs.update({'class': 'form-control'})
