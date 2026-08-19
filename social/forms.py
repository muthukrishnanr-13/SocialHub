from django import forms
from django.contrib.auth.models import User


# =========================
# REGISTER FORM
# =========================

class RegisterForm(forms.ModelForm):

    # Password
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            }
        )
    )

    # Confirm Password
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address'
                }
            ),

        }

    # =========================
    # PASSWORD VALIDATION
    # =========================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data