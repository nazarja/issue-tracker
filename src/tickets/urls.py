from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView

app_name = 'tickets'

urlpatterns = [
    path('bugs/', login_required(TicketListView.as_view()), name='bugs'),
    path('features/', login_required(TicketListView.as_view()), name='features'),
    path('<slug:slug>/details/', login_required(TicketDetailView.as_view()), name='ticket-detail-view'),
    path('create/', login_required(TicketCreateView.as_view()), name='ticket-create-view'),
    path('<slug:slug>/update/', login_required(TicketUpdateView.as_view()), name='ticket-update-view'),
    # path('<slug:slug>/delete/', login_required(TicketDeleteView.as_view()), name='ticket-delete-view'),
]
