from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView, TicketDeleteView

app_name = 'tickets'

urlpatterns = [
    # bugs
    path('bugs/', login_required(TicketListView.as_view()), name='bugs'),
    path('bugs/<slug:slug>/details/', login_required(TicketDetailView.as_view()), name='bugs-details'),
    path('bugs/create', login_required(TicketCreateView.as_view()), name='bugs-create'),
    # features
    path('features/', login_required(TicketListView.as_view()), name='features'),
    path('features/<slug:slug>/details/', login_required(TicketDetailView.as_view()), name='features-details'),
    path('features/create/', login_required(TicketCreateView.as_view()), name='features-create'),
]
