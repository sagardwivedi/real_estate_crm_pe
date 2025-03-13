from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "contact_email", "phone", "address", "website", "description"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Here, you can add custom validation for phone number format
        return phone

    def clean_website(self):
        website = self.cleaned_data.get("website")
        # Custom validation for website can be added here if needed
        return website
