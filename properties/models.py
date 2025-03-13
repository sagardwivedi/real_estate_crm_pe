from django.db import models

from tenants.managers import TenantManager
from tenants.models import Company


class Property(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    address = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    listed_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        indexes = [
            models.Index(fields=["company", "price"]),
            models.Index(fields=["company", "listed_at"]),
        ]
