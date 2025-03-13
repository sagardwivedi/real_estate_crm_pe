from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "status", "assigned_agent"]

        common_classes = "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white dark:border-gray-600"

        widgets = {
            "name": forms.TextInput(
                attrs={"class": f"{common_classes}", "placeholder": "Full Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": f"{common_classes}", "placeholder": "Email Address"}
            ),
            "phone": forms.TextInput(
                attrs={"class": f"{common_classes}", "placeholder": "Phone Number"}
            ),
            "status": forms.Select(
                attrs={"class": f"{common_classes} appearance-none"}
            ),
            "assigned_agent": forms.Select(
                attrs={"class": f"{common_classes} appearance-none"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Lead.objects.filter(email=email).exists():
            raise forms.ValidationError("A lead with this email already exists.")
        return email
