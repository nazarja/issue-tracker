from rest_framework import serializers
from comments.models import Comment
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    current_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'avatar', 'text', 'updated_on', 'current_user')
        read_only_fields = ('id', 'user', 'username', 'avatar', 'updated_on', 'current_user')

    def get_avatar(self, obj):
        return obj.user.profile.avatar

    def get_username(self, obj):
        return obj.user.username

    def get_current_user(self, obj):
        return self.context['request'].user == obj.user


class CommentCreateSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    current_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'avatar', 'updated_on', 'text', 'ticket', 'current_user')
        read_only_fields = ('id', 'user', 'username', 'avatar', 'updated_on', 'current_user')

    def get_avatar(self, obj):
        return obj.user.profile.avatar

    def get_username(self, obj):
        return obj.user.username

    def get_current_user(self, obj):
        return self.context['request'].user == obj.user



