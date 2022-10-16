from oldcore.models import Ticket, Entrada
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['hash', 'client', 'use', 'ticketrequest', 'user', 'event', 'price']


class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = ['pk','name','price', 'isCortesia']