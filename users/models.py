from django.contrib.auth.models import AbstractUser
from django.db import models

from tenants.models import Company


class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("agent", "Agent"),
        ("customer", "Customer"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="admin")

    def __str__(self):
        return f"{self.username} ({self.role})"
