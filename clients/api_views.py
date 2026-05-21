from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from clients.models import Clients, Mailing, Message
from clients.permissions import IsOwnerOrManager
from clients.serializers import ClientSerializer, MailingSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from clients.utils.permissions import is_manager


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if is_manager(self.request.user):
            return Clients.objects.all()
        return Clients.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MailingViewSet(ModelViewSet):
    serializer_class = MailingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if is_manager(self.request.user):
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if is_manager(self.request.user):
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
