from django.contrib.auth.models import BaseUserManager

from tenants.middleware import get_current_company


class TenantManager(BaseUserManager):  # Extending BaseUserManager
    def get_queryset(self):
        company = get_current_company()
        if company:
            return super().get_queryset().filter(company=company)
        return super().get_queryset()

    def get_all_queryset(self):
        return super().get_queryset()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        # Enforce company requirement for non-superusers
        if not user.is_superuser and not extra_fields.get("company"):
            raise ValueError("A company is required for non-superusers.")

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
