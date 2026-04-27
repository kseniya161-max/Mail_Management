from django.urls import path
from documents.views import ClientOfferFileCreateView

app_name = "documents"

urlpatterns = [
    path(
        "client/<int:pk>/offer/create/",
        ClientOfferFileCreateView.as_view(),
        name="client_offer_create",
    ),
]