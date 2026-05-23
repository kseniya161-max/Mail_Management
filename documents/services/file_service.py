from datetime import datetime
from openpyxl import Workbook
from io import BytesIO
from django.core.files.base import ContentFile
from documents.models import OfferFile
import re

import logging

logger = logging.getLogger(__name__)


def slugify_name(name):
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def generate_offer_file(user, products_queryset, file_name=None, client=None):
    """Создает объект OfferFile без генерации Excel файла."""
    if not file_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        first_product = products_queryset.first()

        if first_product:
            base_name = slugify_name(first_product.name[:20])
        else:
            base_name = "offer"

        count = products_queryset.count()

        file_name = f"offer_{base_name}_{count}items_{timestamp}.xlsx"

    if not products_queryset.exists():
        logger.warning(
            f"Пользователь id={user.id} пытался создать товар OfferFile без товаров"
        )

    offer_file = OfferFile.objects.create(
        name=file_name,
        created_by=user,
        client=client,
    )
    logger.info(
        f"Пользователь id={user.id} создал "
        f"OfferFile id={offer_file.id} "
        f"Название файла {file_name} "
        f"products_count={products_queryset.count()}"
    )

    offer_file.products.set(products_queryset)

    return offer_file


def generate_offer_excel(offer):
    """Генерирует Excel файл и сохраняет его в OfferFile."""
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Предложение"

    worksheet.append(["Название", "Категория", "Количество", "Цена", "Описание/сталь"])

    for product in offer.products.all():
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
    file_name = offer.name
    logger.info(f"BEFORE SAVE offer.file.name = {offer.file.name}")
    offer.file.save(file_name, ContentFile(buffer.read()), save=True)
    logger.info(f"AFTER SAVE offer.file = {offer.file.name}")
    logger.info(f"файл Excel id={offer.id} успешно создан")
