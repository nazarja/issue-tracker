from rest_framework import serializers
from comments.models import Comment
from tickets.models import Ticket
from django.conf import settings


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'avatar', 'text', 'updated_on')

    def get_avatar(self, obj):
        return obj.user.profile.avatar

    def get_username(self, obj):
        return obj.user.username


class CommentCreateSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'avatar', 'updated_on', 'text', 'ticket')
        read_only_fields = ('id', 'user', 'username', 'avatar', 'updated_on')

    def get_avatar(self, obj):
        return obj.user.profile.avatar

    def get_username(self, obj):
        return obj.user.username



