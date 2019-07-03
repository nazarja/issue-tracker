from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentListSerializer, CommentCreateSerializer, CommentUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from comments.models import Comment


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListAPIView(ListAPIView):
    lookup_field = 'ticket'
    serializer_class = CommentListSerializer
    ordering = '-updated_on'
    pagination_class = LargeResultsSetPagination
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
    lookup_field = 'id'
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
