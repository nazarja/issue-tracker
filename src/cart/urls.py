from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CartListView, CartCreateView, CartUpdateView

app_name = 'cart'

urlpatterns = [
    path('', login_required(CartListView.as_view()), name='cart'),
    path('create/', login_required(CartCreateView.as_view()), name='cart-create-view'),
    path('update/', login_required(CartUpdateView.as_view()), name='cart-update-view'),
]
