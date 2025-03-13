from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_plan = models.CharField(max_length=100, default="Free")

    def __str__(self):
        return self.name
