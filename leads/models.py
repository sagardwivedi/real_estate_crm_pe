from django.db import models

from tenants.managers import TenantManager
from tenants.models import Company
from users.models import CustomUser


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("negotiation", "Negotiation"),
        ("closed", "Closed"),
        ("lost", "Lost"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    assigned_agent = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Agent"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    objects = TenantManager()

    def __str__(self):
        return self.name
