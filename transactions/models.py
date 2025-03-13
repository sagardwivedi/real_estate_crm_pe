from django.db import models

from properties.models import Property
from tenants.managers import TenantManager


class Transaction(models.Model):
    company_id = models.IntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=255)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        indexes = [
            models.Index(fields=["company_id", "created_at"]),
        ]
