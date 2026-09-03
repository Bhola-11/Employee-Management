from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.executive_analytics_view, name='dashboard'),
    path('dashboard/', views.executive_analytics_view, name='dashboard_alt'),
]
