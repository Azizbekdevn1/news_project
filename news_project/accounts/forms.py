from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label="Parol",widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(label="Parolni takrorlang",widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username', 'first_name','email']

    def clean_passwordConfirm(self):
        data = self.cleaned_data
        if data['password']!=data['passwordConfirm']:
            raise forms.ValidationError("Ikala parolingiz ham bir-biriga teng bo'lishi kerak.")
        return data['passwordConfirm']
