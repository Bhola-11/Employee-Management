from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.executive_analytics_view, name='dashboard'),
]
