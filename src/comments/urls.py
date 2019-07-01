from django.urls import path, include

app_name = 'comments'

urlpatterns = [
    path('api/', include('comments.api.urls'), name='comments.api.urls'),
]
