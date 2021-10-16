from django import forms
from django.core.validators import RegexValidator
from .models import User
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
            
