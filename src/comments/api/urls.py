from django.urls import path
from comments.api.views import CommentListAPIView, CommentCreateAPIView, CommentUpdateAPIView, CommentDeleteAPIView

app_name = 'comments'

urlpatterns = [
    path('<int:ticket>/list/', CommentListAPIView.as_view(), name='comment-list-view'),
    path('<int:ticket>/create/', CommentCreateAPIView.as_view(), name='comment-create-view'),
    path('<int:id>/update/', CommentUpdateAPIView.as_view(), name='comment-update-view'),
    path('<int:id>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete-view'),
]
