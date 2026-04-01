from rest_framework.routers import DefaultRouter

from clients.api_views import ClientViewSet, MailingViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='api-clients')
router.register(r'mailings', MailingViewSet, basename='api-mailings')


urlpatterns = router.urls