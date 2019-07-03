from django.urls import path
from .views import TicketListAPIView, TicketDeleteAPIView, TicketVoteAPIView

urlpatterns = [
    path('list/', TicketListAPIView.as_view(), name='ticket-list-api'),
    path('<int:id>/delete/', TicketDeleteAPIView.as_view(), name='ticket-delete-api'),
    path('<int:id>/vote/', TicketVoteAPIView.as_view(), name='ticket-vote-api'),
]
