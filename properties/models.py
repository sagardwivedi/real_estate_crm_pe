from django.db import models

from tenants.managers import TenantManager


class Property(models.Model):
    company_id = models.IntegerField()
    title = models.CharField(max_length=255)
    address = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    listed_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        indexes = [
            models.Index(fields=["company_id", "price"]),
            models.Index(fields=["company_id", "listed_at"]),
        ]
