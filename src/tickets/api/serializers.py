from rest_framework import serializers
from tickets.models import Ticket
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # fields = '__all__'


class TicketDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket


