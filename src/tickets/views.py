from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Ticket
from .forms import TicketForm
from datetime import datetime


def bug_or_feature(self):
    """
    helper function to determine issue type is a bug or feature
    """
    return 'bug' if 'bug' in self.request.path else 'feature'


class TicketListView(ListView):
    """
    ticket list view, return first 8 tickets,
    counts all tickets to determine if pagination is allowed
    """
    template_name = 'tickets/ticket-list-view.html'
    paginate_by = 8
    extra_context = {}
    allow_empty = True

    def get_queryset(self):
        issue = bug_or_feature(self)
        self.extra_context['issue'] = issue
        self.extra_context['count'] = Ticket.objects.filter(issue=issue).order_by('-updated_on').count()
        return Ticket.objects.filter(issue=issue).order_by('-updated_on')


class TicketDetailView(DetailView):
    """
    renders the tickets details page, figuring out if the current user is the owner
    allows us to check we should show edit and delete controls
    """
    template_name = 'tickets/ticket-detail-view.html'
    extra_context = {'issue': 'issue details', 'already_voted': 'false'}

    def get_object(self, queryset=Ticket):
        # get first ticket with matching id and get the current user
        _id = self.kwargs.get('id')
        instance = Ticket.objects.filter(id=_id).first()
        user = self.request.user

        if instance:
            # dont allow user to vote twice on a bug
            if user in instance.vote_profiles.all():
                self.extra_context['already_voted'] = 'true'
            else:
                self.extra_context['already_voted'] = 'false'
            return instance
        else:
            raise Http404


class TicketCreateView(CreateView):
    """
    renders the create ticket view
    """
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket-create-update-view.html'
    extra_context = {'issue': 'create new ticket', 'button_text': 'create', 'time': datetime.now()}

    def form_valid(self, form):
        """
        on valid form submit we must assign the current user to the ticket instance
        """
        form.instance.user = self.request.user
        form.instance.issue = bug_or_feature(self)
        return super(TicketCreateView, self).form_valid(form)


class TicketUpdateView(UpdateView):
    """
    renders the ticket update / preview view
    get first matching object, on form_valid, save the form.
    """
    form_class = TicketForm
    template_name = 'tickets/ticket-create-update-view.html'
    extra_context = {'issue': 'update ticket', 'button_text': 'update'}

    def get_object(self, queryset=Ticket):
        _id = self.kwargs.get('id')
        return get_object_or_404(Ticket, id=_id)

    def form_valid(self, form):
        return super().form_valid(form)
