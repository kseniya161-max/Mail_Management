import base64
import os

import resend
from django.conf import settings
import sib_api_v3_sdk
from django.core.files.base import ContentFile
from openpyxl import Workbook
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from io import BytesIO
from clients.models import OfferFile


def send_email_via_resend(to_email: str, subject: str, body: str, file=None):
    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": body,
    }

    if file:
        file.seek(0)
        encoded_file = base64.b64encode(file.read()).decode("utf-8")

        params["attachments"] = [
            {
                "filename": os.path.basename(file.name),
                "content": encoded_file,
            }
        ]

    return resend.Emails.send(params)

def send_email_via_brevo(to_email: str, subject: str, body: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={
            "email": settings.BREVO_FROM_EMAIL,
            "name": settings.BREVO_FROM_NAME,
        },
        subject=subject,
        text_content=body,
    )

    return api_instance.send_transac_email(send_smtp_email)


def generate_offer_file(user, products_queryset, file_name=None):
    """Создание файла"""
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

