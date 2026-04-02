from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from clients.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Отправка рассылки'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки на отправку')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            recipients = mailing.recipients.all()

            for recipient in recipients:
                try:
                    send_mail(
                        mailing.message.header,
                        mailing.message.content,
                        'baharevaxen@yandex.ru',
                        [recipient.email],
                    )

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='Успешно',
                        response='Письмо отправлено',
                        attempt_time=timezone.now()
                    )
                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='Не успешно',
                        response=str(e),
                        attempt_time=timezone.now()
                    )

            self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR('Рассылка с таким ID не найдена'))

