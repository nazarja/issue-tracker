from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentListSerializer, CommentCreateSerializer
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework import pagination
from comments.models import Comment


class CommentListAPIView(ListAPIView):
    lookup_field = 'ticket'
    serializer_class = CommentListSerializer
    ordering = '-updated_on'
    pagination.PageNumberPagination.page_size = 100
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        ticket = self.kwargs['ticket']
        return Comment.objects.filter(ticket=ticket).order_by(self.ordering)


class CommentCreateAPIView(CreateAPIView):
    lookup_field = 'ticket'
    queryset = Comment.objects.filter()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentUpdateAPIView(UpdateAPIView):
    pass


class CommentDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
