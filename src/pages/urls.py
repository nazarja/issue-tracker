from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
]
