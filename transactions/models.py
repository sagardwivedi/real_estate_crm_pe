from django.db import models

from properties.models import Property
from tenants.managers import TenantManager
from tenants.models import Company


class Transaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=255)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        indexes = [
            models.Index(fields=["company", "created_at"]),
        ]
