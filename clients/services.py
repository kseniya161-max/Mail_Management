import resend
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

def send_email_via_resend(to_email: str, subject: str, body: str):
    resend.api_key = settings.RESEND_API_KEY

    return resend.Emails.send({
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": body,
    })

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