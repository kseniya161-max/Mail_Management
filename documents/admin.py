from django.contrib import admin

from .models import Invoice, InvoiceItem, InvoiceTemplate, OfferFile


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "client", "created_by", "created_at", "file")
    list_filter = ("created_at", "created_by")
    search_fields = ("number", "client__name")
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice",
        "product_name",
        "quantity",
        "unit",
        "unit_price",
    )
    search_fields = ("product_name",)


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)

@admin.register(OfferFile)
class OfferFileAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "name", "file", "created_at", "get_products")
    search_fields = ("name", "created_by__email")
    list_filter = ("created_at",)

    def get_products(self, obj):
        return ", ".join(product.name for product in obj.products.all())

    get_products.short_description = "Продукты"