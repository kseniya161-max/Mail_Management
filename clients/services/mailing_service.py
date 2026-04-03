from clients.models import MailingAttempt, EmailStatistics
from clients.services.email_service import send_email_via_resend


class MailingService:

    @staticmethod
    def send_mailing(mailing, user):
        success_count = 0
        failed_count = 0

        for recipient in mailing.recipients.all():
            try:
                attached_file = None
                if mailing.message.offer_file and mailing.message.offer_file.file:
                    attached_file = mailing.message.offer_file.file

                response = send_email_via_resend(
                    to_email=recipient.email,
                    subject=mailing.message.header,
                    body=mailing.message.content,
                    file=attached_file,
                )

                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='success',
                    server_response=str(response),
                )
                success_count += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    server_response=str(e),
                )
                failed_count += 1

        EmailStatistics.objects.update_or_create(
            user=user,
            mailing=mailing,
            defaults={
                'success_attempt_mailing': success_count,
                'failed_attempt_mailing': failed_count,
            }
        )

        return success_count, failed_count