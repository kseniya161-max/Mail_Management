from datetime import datetime
from openpyxl import Workbook
from io import BytesIO
from django.core.files.base import ContentFile
from clients.models import OfferFile
import re


def slugify_name(name):
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def generate_offer_file(user, products_queryset, file_name=None, client=None):
    """Создание Excel файла с продуктами"""

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Предложение"

    worksheet.append(["Название", "Категория", "Количество", "Цена", "Описание/сталь"])

    for product in products_queryset:
        worksheet.append(
            [
                product.name,
                product.category.name if product.category else "",
                product.quantity,
                product.price,
                product.description or "",
            ]
        )

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    if not file_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        first_product = products_queryset.first()

        if first_product:
            base_name = slugify_name(first_product.name[:20])
        else:
            base_name = "offer"

        count = products_queryset.count()

        file_name = f"offer_{base_name}_{count}items_{timestamp}.xlsx"

    offer_file = OfferFile.objects.create(
        name=file_name,
        created_by=user,
        client=client,
    )

    offer_file.file.save(file_name, ContentFile(buffer.read()), save=True)

    offer_file.products.set(products_queryset)

    return offer_file
