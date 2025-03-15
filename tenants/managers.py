from django.contrib.auth.models import BaseUserManager

from tenants.middleware import get_current_company


class TenantManager(BaseUserManager):
    """User manager enforcing multi-tenancy based on the current company."""

    def get_queryset(self):
        """Return users filtered by the current company context."""
        company = get_current_company()
        return (
            super().get_queryset().filter(company=company)
            if company
            else super().get_queryset()
        )

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a standard user."""
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)

        if not extra_fields.get("company") and not extra_fields.get("is_superuser"):
            raise ValueError("A company is required for non-superusers.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.update({"is_staff": True, "is_superuser": True})
        return self.create_user(email, password, **extra_fields)
