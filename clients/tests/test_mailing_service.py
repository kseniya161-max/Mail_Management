import pytest
from unittest.mock import patch

from Users.models import User
from clients.models import Clients, Message, Mailing, MailingAttempt, EmailStatistics
from clients.services.mailing_service import MailingService


@pytest.mark.django_db
@patch("clients.services.mailing_service.send_email_via_resend")
def test_send_mailing_success(mock_send_email):
    from django.conf import settings

    settings.RESEND_FROM_EMAIL = "test@example.com"
    settings.RESEND_API_KEY = "test_key"

    mock_send_email.return_value = {"id": "test-id", "status": "sent"}

    user = User.objects.create_user(username="test_user", password="12345")

    client = Clients.objects.create(
        user=user, email="client@test.com", name="Test Client"
    )

    message = Message.objects.create(
        user=user, header="Test header", content="Test content", offer_file=None
    )

    mailing = Mailing.objects.create(user=user, message=message, status="started")
    mailing.recipients.add(client)

    success_count, failed_count = MailingService.send_mailing(mailing, user)

    assert success_count == 1
    assert failed_count == 0

    assert MailingAttempt.objects.count() == 1
    attempt = MailingAttempt.objects.first()
    assert attempt.mailing == mailing
    assert attempt.status == "success"
    assert "sent" in attempt.server_response

    stats = EmailStatistics.objects.get(user=user, mailing=mailing)
    assert stats.success_attempt_mailing == 1
    assert stats.failed_attempt_mailing == 0

    mock_send_email.assert_called_once_with(
        to_email="client@test.com",
        subject="Test header",
        body="Test content",
        file=None,
    )
