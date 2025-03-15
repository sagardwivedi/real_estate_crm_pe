from django.contrib.auth.models import AbstractUser
from django.db import models

from tenants.managers import TenantManager
from tenants.models import Company


class CustomUser(AbstractUser):
    """Custom user model supporting tenant-based filtering."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    theme_preference = models.CharField(
        max_length=10, choices=[("light", "Light"), ("dark", "Dark")], default="light"
    )
    objects = TenantManager()

    def __str__(self):
        return self.username
