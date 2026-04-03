from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from clients.views import HomePageView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls', namespace='clients')),
    path('api/', include('clients.api_urls')),
    path('api/', include('products.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('users/', include('Users.urls', namespace='Users')),
    path('products/', include('products.urls', namespace='products')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

