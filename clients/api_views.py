from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from clients.models import Clients
from clients.permissions import IsOwnerOrManager
from clients.serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return Clients.objects.all()
        return Clients.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

