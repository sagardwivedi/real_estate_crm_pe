from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
