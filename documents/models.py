from decimal import Decimal

from django.db import models

from clients.models import Clients
from config import settings
from products.models import Product


class Invoice(models.Model):
    client = models.ForeignKey(
        Clients, on_delete=models.CASCADE, related_name="invoices"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )
    number = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to="invoices/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vat_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("22.00")
    )

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
        ordering = ["-created_at"]


class InvoiceItem(models.Model):
    UNIT_PIECE = "pcs"
    UNIT_TON = "ton"

    UNIT_CHOICES = [
        (UNIT_PIECE, "шт."),
        (UNIT_TON, "тн"),
    ]
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_PIECE)
    product_name = models.CharField(max_length=255)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=3, default=Decimal("1.000")
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product_name or self.product} × {self.quantity} {self.get_unit_display()}"

    @property
    def total(self):
        return self.quantity * self.unit_price
