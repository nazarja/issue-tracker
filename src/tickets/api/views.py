from rest_framework.generics import ListAPIView, DestroyAPIView
from tickets.models import Ticket
from .permissions import IsOwnerOrReadOnly
from .serializers import TicketListSerializer, TicketDeleteSerializer


class TicketListAPIView(ListAPIView):
    serializer_class = TicketListSerializer

    def get_queryset(self):
        issue = self.request.query_params.get('issue', 'bug')
        order = self.request.query_params.get('order', '-updated_on')
        return Ticket.objects.filter(issue=issue).order_by(order)


class TicketDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Ticket.objects.all()
    serializer_class = TicketDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]
