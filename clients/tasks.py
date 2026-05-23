from celery import shared_task
from clients.services.email_service import send_offer_email, send_invoice_email
from clients.services.mailing_service import MailingService
from documents.models import OfferFile, Invoice
from documents.services.file_service import generate_offer_file, generate_offer_excel
from documents.services.invoice_generator import generate_invoice_docx
from django.utils import timezone
from clients.models import Mailing
import logging


logger = logging.getLogger(__name__)


@shared_task
def send_mailing_task(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    MailingService.send_mailing(mailing, mailing.user)

    mailing.status = "completed"
    mailing.save()


# @shared_task(bind=True, max_retries=3)
# def send_offerfile_task(self, offerfile_id):
#     logger.info(f"START TASK offerfile_id={offerfile_id}")
#     try:
#         offer = OfferFile.objects.get(id=offerfile_id)
#         generate_offer_excel(offer)
#         logger.info(f"BEFORE EMAIL {offer.id}")
#         send_offer_email(offer)
#         logger.info(f"AFTER EMAIL {offer.id}")
#     except Exception as e:
#         logger.error(f"Offer send failed id={offerfile_id}, error={e}")
#         raise self.retry(exc=e, countdown=30)


@shared_task(bind=True, max_retries=3)
def send_offerfile_task(self, offerfile_id):
    try:
        offer = OfferFile.objects.get(id=offerfile_id)

        generate_offer_excel(offer)
        offer.refresh_from_db()

        if not offer.file:
            raise ValueError("Файл offer не был создан")
        send_offer_email(offer)

    except Exception as e:
        logger.error(f"Offer send failed id={offerfile_id}, error={e}")
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


@shared_task
def generate_offer_task(offer_id):
    offer = OfferFile.objects.get(id=offer_id)
    logger.info(f"START EXCEL GENERATION offer={offer.id}")
    generate_offer_excel(offer)
    logger.info(f"FILE SAVED: {offer.file.name}")


@shared_task
def check_and_start_mailings():
    mailings = Mailing.objects.filter(
        status="created",
        datetime_start__lte=timezone.now(),
    )
    for mailing in mailings:
        mailing.status = "started"
        mailing.save()
        send_mailing_task.delay(mailing.id)
