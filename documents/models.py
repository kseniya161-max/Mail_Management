from decimal import Decimal
from django.db import models
from Users.models import User
from config import settings
from products.models import Product


class OfferFile(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название файла")
    client = models.ForeignKey(
        "clients.Clients",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="offer_files",
        verbose_name="Клиент",
    )
    file = models.FileField(upload_to="price_files/", verbose_name="Файл")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Создатель файла"
    )
    products = models.ManyToManyField(Product, verbose_name="Выбранные продукты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "documents_offerfile"

        verbose_name = "Сгенерированный файл"
        verbose_name_plural = "Сгенерированные файлы"



class Invoice(models.Model):
    client = models.ForeignKey(
        "clients.Clients", on_delete=models.CASCADE, related_name="invoices"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )
    number = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to="invoices/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vat_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("22.00")
    )
    is_sent = models.BooleanField(default=False)

    def get_total(self):
        return sum(item.total for item in self.items.all())

    def get_total_with_vat(self):
        subtotal = self.get_total()
        vat = subtotal * (self.vat_rate / Decimal("100"))
        total = subtotal + vat
        return total.quantize(Decimal("0.01"))

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
    product = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.PROTECT
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=3, default=Decimal("1.000")
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product_name or self.product} × {self.quantity} {self.get_unit_display()}"

    @property
    def total(self):
        return self.quantity * self.unit_price


class InvoiceTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название шаблона")
    file = models.FileField(
        upload_to="invoice_templates/",
        verbose_name="Файл шаблона",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Шаблон счёта"
        verbose_name_plural = "Шаблоны счетов"

    def __str__(self):
        return self.name
