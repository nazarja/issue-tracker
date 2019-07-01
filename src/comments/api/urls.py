from django.urls import path, include
from comments.api.views import CommentListAPIView, CommentCreateAPIView, CommentUpdateAPIView, CommentDeleteAPIView

app_name = 'comments'

urlpatterns = [
    path('api/<int:id>list/', CommentListAPIView.as_view(), name='comment-list-view'),
    path('api/create', CommentCreateAPIView.as_view(), name='comment-create-view'),
    path('api/<int:id>/update', CommentUpdateAPIView.as_view(), name='comment-update-view'),
    path('api/<int:id>/delete', CommentDeleteAPIView.as_view(), name='comment-delete-view'),
]
