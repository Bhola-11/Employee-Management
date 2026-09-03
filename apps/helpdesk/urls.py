from django.urls import path
from . import views

app_name = 'helpdesk'

urlpatterns = [
    path('', views.helpdesk_dashboard_view, name='dashboard'),
    path('dashboard/', views.helpdesk_dashboard_view, name='dashboard_alt'),
    path('create/', views.ticket_create_view, name='create'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
