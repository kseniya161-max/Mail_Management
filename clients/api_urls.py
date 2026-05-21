from rest_framework.routers import DefaultRouter

from clients.api_views import ClientViewSet, MailingViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="api-clients")
router.register(r"mailings", MailingViewSet, basename="api-mailings")
router.register(r"messages", MessageViewSet, basename="api-messages")


urlpatterns = router.urls
