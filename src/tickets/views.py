from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bug, Feature


def get_bug_or_feature_queryset(self):
    if 'bugs' in self.request.path:
        self.extra_context['title'] = 'Bugs'
        return Bug.objects.all()
    else:
        self.extra_context['title'] = 'Features'
        return Feature.objects.all()


class TicketListView(ListView):
    template_name = 'tickets/list-ticket-view.html'
    ordering = ['-updated_on']
    paginate_by = 10
    extra_context = {"title": ''}

    def get_queryset(self):
        return get_bug_or_feature_queryset(self)


class TicketDetailView(DetailView):
    template_name = 'tickets/detail-ticket-view.html'
    extra_context = {'title': ''}

    def get_queryset(self):
        return get_bug_or_feature_queryset(self)


class TicketCreateView(CreateView):
    model = Bug
    template_name = 'tickets/create-update-ticket-view.html'


class TicketUpdateView(UpdateView):
    pass


class TicketDeleteView(DeleteView):
    pass

