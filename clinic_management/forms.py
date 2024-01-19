from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class DoctorLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('doctor_username')
        if username:
            self.user_cache = authenticate(self.request, username=username, password=cleaned_data.get('password'))
            if self.user_cache is None:
                raise self.get_invalid_login_error()
        return cleaned_data

