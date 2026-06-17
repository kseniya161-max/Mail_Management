import base64
import os
import resend
import sib_api_v3_sdk
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


def send_email_via_resend(to_email: str, subject: str, body: str, file=None):
    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": f"{settings.EMAIL_FROM_NAME} <{settings.RESEND_FROM_EMAIL}>",
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

    try:
        logger.info(f"Отправка email на {to_email}")

        response = resend.Emails.send(params)

        logger.info(f"Email успешно отправлен на {to_email}")

        return response

    except Exception as e:
        logger.error(f"Ошибка отправки email на {to_email}: {e}")
        try:
            logger.warning(f"Пробуем fallback отправку на email={to_email}")

            params["from"] = settings.RESEND_FROM_EMAIL

            response = resend.Emails.send(params)
            logger.info(f"Письмо успешно ушло на email={to_email}")

            return response

        except Exception as fallback_error:
            logger.critical(f"fallback отправка упала для {to_email}: {fallback_error}")
            raise


def send_email_via_brevo(to_email: str, subject: str, body: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

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


def send_invoice_email(invoice):
    client = invoice.client
    logger.info(f"Отправка Invoice id={invoice.id} клиенту {client.email}")
    if not client.email:
        logger.error(f"У клиента id={client.id} нет email")
        raise ValueError("У клиента нет email")
    if not invoice.file:
        logger.error(f"У Invoice id={invoice.id} не вложен файл")
        raise ValueError("У счета нет файла")
    with open(invoice.file.path, "rb") as f:
        send_email_via_resend(
            to_email=client.email,
            subject=f"Счет № {invoice.number}",
            body="Добрый день! Во вложении ваш счет.",
            file=f,
        )
        logger.info(f"Отправка Invoice id={invoice.id} успешно отправлен")


def send_offer_email(offer):
    client = offer.client
    logger.info(f"Отправка OfferFile id={offer.id} клиенту {client.email}")

    if not client.email:
        logger.error(f"У клиента id={client.id} нет email")
        raise ValueError("У клиента нет email")

    if not offer.file:
        logger.error(f"У предложения id={offer.id} нет файла")
        raise ValueError("Нет файла предложения")

    with open(offer.file.path, "rb") as f:
        send_email_via_resend(
            to_email=client.email,
            subject="Коммерческое предложение",
            body="Добрый день! Во вложении предложение.",
            file=f,
        )
        logger.info(f"OfferFile id={offer.id} успешно отправлен")
