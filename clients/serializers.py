from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from clients.models import Clients, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ["id", "email", "name", "comment", "location"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = [
            "id",
            "recipients",
            "message",
            "status",
            "datetime_start",
            "datetime_end",
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "user",
            "header",
            "content",
            "product",
            "offer_file",
        ]
        read_only_fields = ["user"]
