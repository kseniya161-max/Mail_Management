from django.contrib.admin import views
from django.urls import path, include
from clients.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    EmailStatisticsView,
)
from clients.views import (
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    HomePageView,
    UserOfferFilesView,
)
from clients.views import (
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingSendView,
)
from clients.views import (
    ManegerClientListView,
    UserProfileView,
    UserProfileUpdateView,
    DeactivateMailingView,
    DeactivateMailingConfirmView,
    OfferFileDeleteView,
)
from clients.views import OfferFileCreateView

app_name = "clients"

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("client/add/", ClientCreateView.as_view(), name="client_add"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/add/", MessageCreateView.as_view(), name="message_add"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/add/", MailingCreateView.as_view(), name="mailing_add"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("mailing/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path("home/", HomePageView.as_view(), name="home"),
    path("statistic/", EmailStatisticsView.as_view(), name="email_statistic"),
    path(
        "manager/clients/", ManegerClientListView.as_view(), name="manager_client_list"
    ),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="user_profile_edit"),
    path(
        "mailing/<int:mailing_id>/deactivate/",
        DeactivateMailingView.as_view(),
        name="deactivate_mailing",
    ),
    path(
        "mailing/<int:mailing_id>/deactivate/confirm/",
        DeactivateMailingConfirmView.as_view(),
        name="deactivate_mailing_confirm",
    ),
    path("offer-file/create/", OfferFileCreateView.as_view(), name="offer_file_create"),
    path("my-offers/", UserOfferFilesView.as_view(), name="my_offers"),
    path(
        "my-offers/delete/<int:pk>/", OfferFileDeleteView.as_view(), name="offer_delete"
    ),
]
