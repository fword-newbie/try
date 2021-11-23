from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import People


class RegisterForm(forms.Form):
    account = forms.CharField(
        label="account",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    phone = forms.CharField(
        label="phone",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    email = forms.CharField(
        label="email",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    password = forms.CharField(
        label="password",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = People
        fields = ('phone', 'email','password')

# class loginform(forms.Form):
#     account = forms.CharField(
#         label="account",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False
#     )
#     password = forms.CharField(
#         label="password",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#     )
#     class Meta:
#         model = People
#         fields = ('password')
