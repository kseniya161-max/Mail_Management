from celery import shared_task
from clients.models import Mailing
from clients.services.email_service import send_offer_email
from clients.services.mailing_service import MailingService
from documents.models import OfferFile


@shared_task
def send_mailing_task(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    MailingService.send_mailing(mailing, mailing.user)

    mailing.status = "completed"
    mailing.save()


@shared_task(bind=True, max_retries=3)
def send_offerfile_task(self,offerfile_id):
    try:
        offer = OfferFile.objects.get(id=offerfile_id)
        send_offer_email(offer)
    except Exception as e:
        raise self.retry(exc=e, countdown=30)
