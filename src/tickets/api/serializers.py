from rest_framework import serializers
from tickets.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'avatar', 'title', 'description', 'status', 'votes', 'created_on', 'updated_on', 'cost', 'earned', 'issue', 'slug',)

    def get_avatar(self, obj):
        return obj.user.profile.avatar


class TicketDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket


