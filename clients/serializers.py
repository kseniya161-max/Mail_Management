from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from clients.models import Clients


class ClientSerializer(serializers, ModelSerializer):
    class Meta:
        model = Clients
        fields = ['user', 'email', 'name', 'comment', 'location']