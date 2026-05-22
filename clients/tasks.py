from celery import shared_task
from clients.models import Mailing
from clients.services.email_service import send_offer_email, send_invoice_email
from clients.services.mailing_service import MailingService
from documents.models import OfferFile, Invoice
from documents.services.file_service import generate_offer_file
from documents.services.invoice_generator import generate_invoice_docx


@shared_task
def send_mailing_task(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    MailingService.send_mailing(mailing, mailing.user)

    mailing.status = "completed"
    mailing.save()


@shared_task(bind=True, max_retries=3)
def send_offerfile_task(self, offerfile_id):
    try:
        offer = OfferFile.objects.get(id=offerfile_id)
        send_offer_email(offer)
    except Exception as e:
        raise self.retry(exc=e, countdown=30)


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 30},
)
def send_invoice_task(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    send_invoice_email(invoice)


@shared_task
def generate_invoice_task(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    generate_invoice_docx(invoice)


# @shared_task
# def generate_offer_task(offer_id):
#     offer = OfferFile.objects.get(id=offer_id)
#     generate_offer_file(offer)
