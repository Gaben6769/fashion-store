from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Форма реєстрації нового користувача."""

    email = forms.EmailField(
        required=True,
        label="Електронна пошта",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Ваша електронна пошта",
                "autocomplete": "email",
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        label="Ім'я",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше ім'я",
                "autocomplete": "given-name",
            }
        ),
    )

    last_name = forms.CharField(
        required=False,
        label="Прізвище",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше прізвище",
                "autocomplete": "family-name",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

        labels = {
            "username": "Ім'я користувача",
            "password1": "Пароль",
            "password2": "Підтвердження пароля",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Введіть ім'я користувача",
                    "autocomplete": "username",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "placeholder": "Введіть пароль",
                    "autocomplete": "new-password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "placeholder": "Повторіть пароль",
                    "autocomplete": "new-password",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Користувач із такою електронною поштою вже існує."
            )

        return email


class UkrainianAuthenticationForm(AuthenticationForm):
    """Форма входу українською мовою."""

    username = forms.CharField(
        label="Ім'я користувача",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введіть ім'я користувача",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введіть пароль",
                "autocomplete": "current-password",
            }
        ),
    )