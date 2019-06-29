from rest_framework.generics import ListAPIView, DestroyAPIView
from .serializers import TicketListSerializer, TicketDeleteSerializer
from .permissions import IsOwnerOrReadOnly
from tickets.models import Ticket
from django.db.models import Q


class TicketListAPIView(ListAPIView):
    serializer_class = TicketListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        issue = self.request.query_params.get('issue', 'bug')
        order = self.request.query_params.get('order', '-updated_on')

        if query is not None:
            return Ticket.objects.filter(
                Q(title__iexact=query, issue=issue) | Q(description__icontains=query, issue=issue)
            ).order_by(order)

        return Ticket.objects.filter(issue=issue).order_by(order)


class TicketDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Ticket.objects.all()
    serializer_class = TicketDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]
