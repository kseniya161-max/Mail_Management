from datetime import timedelta

from django.db import models
from django.db.models import PositiveIntegerField
from django.utils import timezone

from Users.models import User
from products.models import Product


class Clients(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length = 100)
    comment = models.TextField(blank=True)
    location = models.CharField(max_length = 100, null=True, verbose_name='Укажите город')

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("can_manage_clients", "Can manage clients"),
        ]


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    header = models.CharField(max_length=200)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Наименование товара')

    def __str__(self):
        return self.header

    class Meta:
        permissions = [
            ("can_manage_message", "Can manage message"),
        ]


class Mailing(models.Model):
    """ Модель рассылки"""
    STATUS_CHOICES = [('created', 'создана'),
                      ('started', 'запущена'),
                      ('completed', 'завершена'),
                      ('closed', 'отключена')]

    datetime_start = models. DateTimeField(default=timezone.now)
    datetime_end = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Clients)
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рассылка: {self.message.header}  - Статус: {self.get_status_display()}'

    class Meta:
        permissions = [
            ("can_manage_mailing", "Can manage mailing"),
        ]


class MailingAttempt(models.Model):
    """ Модель попытки рассылок"""
    STATUS_CHOICES = [('success', 'успешно'),
                      ('failed', 'неуспешно'),]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True)

    def __str__(self):
        return f'Попытка рассылки: {self.status} - {self.attempt_time}'

    class Meta:
        permissions = [
            ("can_manage_mailing", "Can manage mailing"),
        ]


class EmailStatistics(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    success_attempt_mailing = models.PositiveIntegerField(default=0)
    failed_attempt_mailing = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Количество успешных рассылок{self.success_attempt_mailing}, Количество неуспешных рассылок{self.failed_attempt_mailing}'


