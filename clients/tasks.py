from celery import shared_task
from clients.models import Mailing
from clients.services.mailing_service import MailingService


@shared_task
def send_mailing_task(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    MailingService.send_mailing(mailing, mailing.user)

    mailing.status = "completed"
    mailing.save()
