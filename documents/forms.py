from django.forms import inlineformset_factory

from documents.models import Invoice, InvoiceItem
from django import forms


class InvoiceForm(forms.ModelForm):
    """Форма Создания клиента"""

    class Meta:
        model = Invoice
        fields = ["number"]

    widgets = {
        "number": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Например: 001/2026",
            }
        )
    }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ["product", "quantity", "unit", "unit_price"]
        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.001",
                    "min": "0",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }


InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=3,
    can_delete=True,
)
