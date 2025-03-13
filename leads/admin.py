from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "assigned_agent", "created_at")
    list_filter = ("status", "assigned_agent")
    search_fields = ("name", "email", "phone")
