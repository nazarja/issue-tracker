from rest_framework import serializers
from tickets.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
    """
    ticket list serializer, return ticket with additional method field,
    the avatar, for easy access to display along side the ticket
    """
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'username', 'avatar', 'title', 'description', 'status', 'votes', 'created_on', 'updated_on', 'earned', 'issue', 'slug',)

    def get_avatar(self, obj):
        # return avatar to display on ticket item
        return obj.user.profile.avatar


class TicketDeleteSerializer(serializers.ModelSerializer):
    """
    delete serializer just needs basic ticket model with no additional requirements
    """
    class Meta:
        model = Ticket

