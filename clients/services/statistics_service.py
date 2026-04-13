from django.db.models import Sum
from clients.models import EmailStatistics


def get_email_statistics_for_user(user):
    if user.role == "manager":
        return (
            EmailStatistics.objects.select_related("mailing")
            .values("mailing__message__header", "mailing__status", "user__username")
            .annotate(
                total_success=Sum("success_attempt_mailing"),
                total_failed=Sum("failed_attempt_mailing"),
            )
            .order_by("mailing__message__header")
        )
    return (
        EmailStatistics.objects.filter(user=user)
        .select_related("mailing")
        .values("mailing__message__header", "mailing__status", "user__username")
        .annotate(
            total_success=Sum("success_attempt_mailing"),
            total_failed=Sum("failed_attempt_mailing"),
        )
        .order_by("mailing__message__header")
    )


def get_email_statistics_summary(statistics):
    total_success = sum(stat["total_success"] for stat in statistics)
    total_failed = sum(stat["total_failed"] for stat in statistics)

    return {
        "total_success": total_success,
        "total_failed": total_failed,
        "total_attempts": total_success + total_failed,
    }
