from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .permissions import IsOwnerOrReadOnly
from comments.models import Comment


class CommentListAPIView(ListAPIView):
    pass


class CommentCreateAPIView(CreateAPIView):
    pass


class CommentUpdateAPIView(UpdateAPIView):
    pass


class CommentDeleteAPIView(DestroyAPIView):
    pass