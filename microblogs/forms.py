from django import forms
from .models import User
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets= {'bio': forms.Textarea() }

    new_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    passowrd_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())
