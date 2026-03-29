from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from clients.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls', namespace='clients')),
    path('', HomePageView.as_view(), name='home'),
    path('users/', include('Users.urls', namespace='Users')),
    path('products/', include('products.urls', namespace='products')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)