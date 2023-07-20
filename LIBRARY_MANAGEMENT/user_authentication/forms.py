from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class SingUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}),help_text="enter first name")
    last_name = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]


class ChagneUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
        
        
