from django.urls import path
from documents.views import (
    ClientOfferFileCreateView,
    ClientOfferFilesView,
    InvoiceCreateView,
    ClientInvoiceListView,
    InvoiceDeleteView,
    InvoiceSendView,
    ClientOfferDeleteView,
    ClientOfferSendView,
)

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
        "offers/<int:pk>/delete/",
        ClientOfferDeleteView.as_view(),
        name="offer_delete",
    ),
    path(
        "offers/<int:pk>/send/",
        ClientOfferSendView.as_view(),
        name="offer_send",
    ),
    path(
        "clients/<int:client_id>/invoice/create/",
        InvoiceCreateView.as_view(),
        name="invoice_create",
    ),
    path(
        "clients/<int:client_id>/invoice/",
        ClientInvoiceListView.as_view(),
        name="client_invoices",
    ),
    path(
        "invoices/<int:pk>/delete/",
        InvoiceDeleteView.as_view(),
        name="invoice_delete",
    ),
    path(
        "invoices/<int:pk>/send/",
        InvoiceSendView.as_view(),
        name="invoice_send",
    ),
]
