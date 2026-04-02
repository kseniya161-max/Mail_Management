
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from Users.models import User
# from .models import Clients, Message, Mailing, EmailStatistics
#
# admin.site.register(Clients)
# admin.site.register(Message)
# admin.site.register(Mailing)
# admin.site.register(EmailStatistics)


from django.contrib import admin
from clients.models import Clients, Message, Mailing, MailingAttempt, EmailStatistics, OfferFile


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user', 'location')
    search_fields = ('name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'user', 'product')
    search_fields = ('header',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'status', 'user', 'datetime_start', 'datetime_end')
    list_filter = ('status',)
    search_fields = ('message__header',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'status', 'attempt_time', 'server_response')
    list_filter = ('status', 'attempt_time')
    search_fields = ('server_response',)


@admin.register(EmailStatistics)
class EmailStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mailing', 'success_attempt_mailing', 'failed_attempt_mailing')




@admin.register(OfferFile)
class OfferFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'name', 'file', 'created_at', 'get_products')
    search_fields = ('name', 'created_by__email')
    list_filter = ('created_at',)

    def get_products(self, obj):
        return ", ".join(product.name for product in obj.products.all())

    get_products.short_description = 'Продукты'