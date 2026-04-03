from openpyxl import Workbook
from io import BytesIO
from django.core.files.base import ContentFile
from clients.models import OfferFile


def generate_offer_file(user, products_queryset, file_name=None):
    """Создание Excel файла с продуктами"""

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Предложение'

    worksheet.append(['Название', 'Категория', 'Количество', 'Описание'])

    for product in products_queryset:
        worksheet.append([
            product.name,
            product.category.name if product.category else '',
            product.quantity,
            product.description or '',
        ])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    if not file_name:
        file_name = 'offer_file.xlsx'

    offer_file = OfferFile.objects.create(
        name=file_name,
        created_by=user,
    )

    offer_file.file.save(
        file_name,
        ContentFile(buffer.read()),
        save=True
    )

    offer_file.products.set(products_queryset)

    return offer_file