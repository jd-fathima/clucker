from django.utils import timezone
from django import forms
from django.core.validators import RegexValidator
from .models import User,Post
from django.db import models

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {'text':forms.Textarea()}

    def printText(self):
        super.save(commit=True)
        text = self.cleaned_data.get('text')
        print(text)

class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets= {'bio': forms.Textarea() }

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$', # positive look ahead is ?=
            message = 'Password must contain an uppercase, a lowercase character and a number'
        )
            # RegexValidator(
            #     regex=r'[A-Z]',
            #     message='Password must contain an uppercase character.'
            # ),
            # RegexValidator(
            #     regex=r'[a-z]',
            #     message='Password must contain a lowercase character.'
            # ),
            # RegexValidator(
            #     regex=r'[0-9]',
            #     message='Password must contain a number character.'
            # ),
        ]
    )
    password_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password= self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password')

    def save(self):
        super().save(commit=False)#does everything it normally does except storing the data
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            password = self.cleaned_data.get('new_password'),
        )
        return user
