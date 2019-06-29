from django.urls import path
from .views import TicketListAPIView, TicketDeleteAPIView

urlpatterns = [
    path('list/', TicketListAPIView.as_view(), name='ticket-list-api'),
    path('<int:id>/delete/', TicketDeleteAPIView.as_view(), name='ticket-delete-api'),
]
