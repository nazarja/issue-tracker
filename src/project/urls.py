from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('activity-feed/', include('activity_feed.urls')),
    path('cart/', include('cart.urls')),
    path('charts/', include('charts.urls')),
    path('checkout/', include('checkout.urls')),
    path('contact/', include('contact.urls')),
    path('comments/', include('comments.urls')),
    path('profiles/', include('profiles.urls')),
    path('tickets/', include('tickets.urls')),
]

