from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import Customer
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

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
        return user
    
class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser']

class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
        return cleaned_data