from django.db import models

from tenants.middleware import get_current_company


class TenantManager(models.Manager):
    def get_queryset(self):
        company_id = get_current_company()
        if company_id:
            return super().get_queryset().filter(company_id=company_id)
        return super().get_queryset()

    def get_all_queryset(self):
        """Bypasses tenant filtering for admin reports."""
        return super().get_queryset()
