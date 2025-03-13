from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Company, CustomUser


class CompanySignupForm(forms.ModelForm):
    """Form for registering a new real estate company with improved Tailwind styling."""

    class Meta:
        model = Company
        fields = ["name", "contact_email", "phone"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Company Name",
                    "aria-label": "Company Name",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Company Email",
                    "aria-label": "Company Email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Company Phone Number",
                    "aria-label": "Company Phone",
                }
            ),
        }


class AdminSignupForm(UserCreationForm):
    """Admin user registration with Tailwind styling."""

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                "placeholder": "Full Name",
                "aria-label": "Full Name",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Email Address",
                    "aria-label": "Email Address",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Create Password",
                    "aria-label": "Create Password",
                    "autocomplete": "new-password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                    "placeholder": "Confirm Password",
                    "aria-label": "Confirm Password",
                    "autocomplete": "new-password",
                }
            ),
        }

    def save(self, company, commit=True):
        """Save method to associate admin with the company."""
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.company = company
        user.role = "admin"
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    """Custom login form with improved Tailwind styling."""

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                "placeholder": "Enter your email",
                "aria-label": "Email",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 dark:text-white",
                "placeholder": "Enter your password",
                "aria-label": "Password",
                "autocomplete": "current-password",
            }
        )
    )

    def confirm_login_allowed(self, user):
        """Ensure only active users can log in."""
        if not user.is_active:
            raise ValidationError(
                "This account is inactive. Please contact support.",
                code="inactive",
            )
