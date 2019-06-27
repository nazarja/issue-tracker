from django.urls import path
from django.views.generic import TemplateView
from .views import IndexView

app_name = 'pages'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
]
