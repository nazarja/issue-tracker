from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentListSerializer, CommentCreateSerializer, CommentUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from comments.models import Comment


class LargeResultsSetPagination(PageNumberPagination):
    """
    custom pagination class for comments
    normally, 8 results is set by default in base.py
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListAPIView(ListAPIView):
    """
    queries the comments model for comments with the same ticket id
    as the kwarg sent in the url, returns all comments queryset
    """
    lookup_field = 'ticket'
    serializer_class = CommentListSerializer
    ordering = '-updated_on'
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        ticket = self.kwargs['ticket']
        return Comment.objects.filter(ticket=ticket).order_by(self.ordering)


class CommentCreateAPIView(CreateAPIView):
    """
    creates a new comment
    """
    lookup_field = 'ticket'
    queryset = Comment.objects.filter()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        """
        pass the current user to the serializer instance and save
        """
        serializer.save(user=self.request.user)


class CommentUpdateAPIView(UpdateAPIView):
    """
    updates a comments text field
    """
    lookup_field = 'id'
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteAPIView(DestroyAPIView):
    """
    deletes a comment, must be owner to perform this action
    """
    lookup_field = 'id'
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
