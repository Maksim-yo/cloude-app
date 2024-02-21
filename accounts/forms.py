from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Profile


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'form':'update_avatar', 'class': 'form-control mb-1 '}))

    class Meta:
        model = Profile
        fields = ['avatar']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control mb-1',
                                       'placeholder': 'Username'}))
    password = forms.CharField(max_length=30, required=True,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control mb-1',
                                       'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control mb-1',
                                       'placeholder': 'Enter Username'}))
    password1 = forms.CharField(max_length=30, label="Password",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control mb-1',
                                        'placeholder': 'Enter password'}))
    password2 = forms.CharField(max_length=30, label="Repeat password",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control mb-1',
                                        'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30,
                               required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control mb-1',
                                       'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ['username', 'email']

