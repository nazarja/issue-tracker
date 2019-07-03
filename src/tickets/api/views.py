from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TicketListSerializer, TicketDeleteSerializer
from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from django.db.models import Q
from tickets.models import Ticket


class TicketListAPIView(ListAPIView):
    serializer_class = TicketListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        issue = self.request.query_params.get('issue', 'bug')
        order = self.request.query_params.get('order', '-updated_on')

        # filter choices
        if order in ['need help', 'in progress', 'resolved']:
            status = order

            # filter choices and query together
            if query is not None:
                return Ticket.objects.filter(
                    Q(title__icontains=query, issue=issue, status=status) | Q(description__icontains=query, issue=issue, status=status)
                ).order_by('-updated_on')

            # return only filtered choices
            return Ticket.objects.filter(issue=issue, status=status).order_by('-updated_on')

        # if a query is passed
        if query is not None:
            return Ticket.objects.filter(
                Q(title__icontains=query, issue=issue) | Q(description__icontains=query, issue=issue)
            ).order_by(order)

        # no query - no choices - generic order by
        return Ticket.objects.filter(issue=issue).order_by(order)


class TicketDeleteAPIView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Ticket.objects.all()
    serializer_class = TicketDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TicketVoteAPIView(APIView):

    def get_object(self, _id):
        try:
            return Ticket.objects.get(id=_id)
        except Ticket.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        instance = self.get_object(id)
        user = self.request.user

        if user in instance.vote_profiles.all():
            return Response({'text': 'already voted for this', 'votes': instance.votes})
        else:
            instance.votes += 1
            instance.vote_profiles.add(user)
            instance.save()
            return Response({'text': 'ok', 'votes': instance.votes})

