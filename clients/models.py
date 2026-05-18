from datetime import timedelta
from django.db import models
from django.db.models import PositiveIntegerField, CharField
from django.utils import timezone
from Users.models import User
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField

class City(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]


class Clients(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    location = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Укажите город",
    )
    phone_number = PhoneNumberField(
        region="RU",
        blank=False,
        null=False,
        verbose_name="Номер телефона",
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    header = models.CharField(max_length=200, verbose_name="Заголовок сообщения")
    content = models.TextField(verbose_name="Сообщение")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Наименование товара",
    )
    offer_file = models.ForeignKey(
        "documents.OfferFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Прикрепленный файл",
    )

    def __str__(self):
        return self.header


def get_default_end_date():
    return timezone.now() + timedelta(days=1)


class Mailing(models.Model):
    """Модель рассылки"""

    STATUS_CHOICES = [
        ("created", "создана"),
        ("started", "запущена"),
        ("completed", "завершена"),
        ("closed", "отключена"),
    ]

    datetime_start = models.DateTimeField(default=timezone.now)
    datetime_end = models.DateTimeField(default=get_default_end_date)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Clients)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Рассылка: {self.message.header}  - Статус: {self.get_status_display()}"


class MailingAttempt(models.Model):
    """Модель попытки рассылок"""

    STATUS_CHOICES = [
        ("success", "успешно"),
        ("failed", "неуспешно"),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True)

    def __str__(self):
        return f"Попытка рассылки: {self.status} - {self.attempt_time}"


class EmailStatistics(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    success_attempt_mailing = models.PositiveIntegerField(default=0)
    failed_attempt_mailing = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Количество успешных рассылок{self.success_attempt_mailing}, Количество неуспешных рассылок{self.failed_attempt_mailing}"
