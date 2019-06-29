from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView

app_name = 'tickets'

urlpatterns = [
    path('bugs/', login_required(TicketListView.as_view()), name='bugs'),
    path('features/', login_required(TicketListView.as_view()), name='features'),
    path('<int:id>/<slug:slug>/details/', login_required(TicketDetailView.as_view()), name='ticket-detail-view'),
    path('create/', login_required(TicketCreateView.as_view()), name='ticket-create-view'),
    path('<int:id>/<slug:slug>/update/', login_required(TicketUpdateView.as_view()), name='ticket-update-view'),
    path('api/', include('tickets.api.urls'), name='tickets.api.urls'),
]
