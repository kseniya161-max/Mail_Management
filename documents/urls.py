from django.urls import path
from documents.views import ClientOfferFileCreateView, ClientOfferFilesView, InvoiceCreateView

app_name = "documents"

urlpatterns = [
    path(
        "client/<int:pk>/offer/create/",
        ClientOfferFileCreateView.as_view(),
        name="client_offer_create",
    ),
    path(
        "client/<int:pk>/offers/",
        ClientOfferFilesView.as_view(),
        name="client_offer_files",
    ),
    path(
        "clients/<int:client_id>/invoice/create/",
        InvoiceCreateView.as_view(),
        name="invoice_create",
    ),
]
