from rest_framework.generics import ListAPIView, DestroyAPIView
from tickets.models import Ticket
from .permissions import IsOwnerOrReadOnly
from .serializers import TicketSerializer


class TicketListAPIView(ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly]
