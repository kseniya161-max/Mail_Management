import base64
import os
import resend
import sib_api_v3_sdk
from django.conf import settings


def send_email_via_resend(to_email: str, subject: str, body: str, file=None):
    resend.api_key = settings.RESEND_API_KEY
    print("API KEY:", settings.RESEND_API_KEY[:10])

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
        print("SENDING EMAIL:", params)

        response = resend.Emails.send(params)

        print("RESEND RESPONSE:", response)

        return response

    except Exception as e:
        print("RESEND ERROR:", e)

        params["from"] = settings.RESEND_FROM_EMAIL

        response = resend.Emails.send(params)

        print("RESEND FALLBACK RESPONSE:", response)

        return response


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
    if not client.email:
        raise ValueError("У клиента нет email")
    if not invoice.file:
        raise ValueError("У счета нет файла")
    with open(invoice.file.path, "rb") as f:
        send_email_via_resend(
            to_email=client.email,
            subject=f"Счет № {invoice.number}",
            body="Добрый день! Во вложении ваш счет.",
            file=f,
        )