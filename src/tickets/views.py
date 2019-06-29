from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Ticket
from .forms import TicketForm


def bug_or_feature(self):
    return 'bug' if 'bug' in self.request.path else 'feature'


class TicketListView(ListView):
    template_name = 'tickets/ticket-list-view.html'
    paginate_by = 10
    extra_context = {}
    allow_empty = True

    def get_queryset(self):
        issue = bug_or_feature(self)
        self.extra_context['issue'] = issue
        return Ticket.objects.filter(issue=issue).order_by('-updated_on')


class TicketDetailView(DetailView):
    template_name = 'tickets/ticket-detail-view.html'
    extra_context = {'issue': 'issue details'}

    def get_object(self, queryset=Ticket):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Ticket, slug=slug)


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket-create-update-view.html'
    extra_context = {'issue': 'create new ticket'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketUpdateView(UpdateView):
    form_class = TicketForm
    template_name = 'tickets/ticket-create-update-view.html'
    extra_context = {'issue': 'update ticket'}

    def get_object(self, queryset=Ticket):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Ticket, slug=slug)

    def form_valid(self, form):
        return super().form_valid(form)
