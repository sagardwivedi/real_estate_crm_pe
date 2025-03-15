from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Company, CustomUser


class TailwindStyledFormMixin:
    """Provides Tailwind CSS styling for form fields."""

    form_control_class = (
        "w-full px-4 py-3 border border-gray-300 dark:border-gray-600 "
        "rounded-lg bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 "
        "focus:outline-none text-gray-900 dark:text-white transition duration-200 ease-in-out"
    )

    def apply_tailwind_classes(self, fields):
        """Applies Tailwind styles and placeholders to form fields."""
        placeholders = {
            "name": "Enter company name",
            "contact_email": "Enter company email",
            "phone": "Enter company phone number",
            "first_name": "Enter your first name",
            "last_name": "Enter your last name",
            "email": "Enter your email address",
            "password1": "Create a password",
            "password2": "Confirm your password",
            "username": "Enter your username",
            "password": "Enter your password",
        }

        for field_name in fields:
            field = self.fields[field_name]
            field.widget.attrs["class"] = self.form_control_class
            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]


class BaseUserForm(forms.ModelForm, TailwindStyledFormMixin):
    """Abstract base form for user-related forms."""

    def clean_email(self):
        """Ensure the email is unique and set as the username."""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        """Ensure username is set as email before saving."""
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CompanySignupForm(forms.ModelForm, TailwindStyledFormMixin):
    """Form for registering a new real estate company."""

    class Meta:
        model = Company
        fields = ["name", "contact_email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(self.fields)


class AdminSignupForm(UserCreationForm, TailwindStyledFormMixin):
    """Admin user registration form."""

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(self.fields)


class CustomLoginForm(AuthenticationForm, TailwindStyledFormMixin):
    """Custom login form with Tailwind styling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(["username", "password"])

    def confirm_login_allowed(self, user):
        """Ensure only active users can log in."""
        if not user.is_active:
            raise ValidationError(
                "This account is inactive. Please contact support.",
                code="inactive",
            )


class UserCreateForm(BaseUserForm):
    """Form for creating a new user."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Create a password"})
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(self.fields)

    def clean(self):
        """Ensure passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = self.data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        return cleaned_data


class UserEditForm(BaseUserForm):
    """Form for editing user details."""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(self.fields)
