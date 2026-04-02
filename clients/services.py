import resend
from django.conf import settings


def send_email_via_resend(to_email: str, subject: str, body: str):
    resend.api_key = settings.RESEND_API_KEY

    return resend.Emails.send({
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": body,
    })