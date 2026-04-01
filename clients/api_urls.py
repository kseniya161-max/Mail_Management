from rest_framework.routers import DefaultRouter

from clients.api_views import ClientViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='api-clients')

urlpatterns = router.urls