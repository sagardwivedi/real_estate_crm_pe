from django.contrib import admin

from properties.models import Property


class PropertyAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Property.objects.get_all_queryset()
        return super().get_queryset(request)


admin.site.register(Property, PropertyAdmin)
