from django import forms

from users.forms import TailwindStyledFormMixin


class ReportFilterForm(forms.Form, TailwindStyledFormMixin):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    role = forms.ChoiceField(
        choices=[("", "All Roles"), ("admin", "Admin"), ("agent", "Agent")],
        required=False,
    )
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes(["start_date", "end_date", "role", "email"])
