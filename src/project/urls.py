from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('activity-feed/', include('activity_feed.urls')),
    path('charts/', include('charts.urls')),
    path('profiles/', include('profiles.urls')),
    path('tickets/', include('tickets.urls')),
]

