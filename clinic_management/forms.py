from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Doctor, Patient, Department

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# class PostDoctor(forms.ModelForm):
#     doctor_phone = forms.CharField(max_length=15, required=True)
#     department_name = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.save()

#         doctor = Doctor.objects.create(
#             user=user,
#             doctor_phone=self.cleaned_data['doctor_phone'],
#             department_name=self.cleaned_data['department_name']
#         )

#         return user
    

# class PostPatient(forms.ModelForm):
#     class Meta: 
#         model = Patient
#         fields = ['username', 'password1', 'password2', 'fisrt_name', 'last_name', 'patient_phone']


# class DoctorLoginForm(AuthenticationForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'] = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('doctor_username')
#         if username:
#             self.user_cache = authenticate(self.request, username=username, password=cleaned_data.get('password'))
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#         return cleaned_data

