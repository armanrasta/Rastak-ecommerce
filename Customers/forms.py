from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()


class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=63)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
