from django.urls import path
from . import views

app_name = 'leave_management'

urlpatterns = [
    path('dashboard/', views.leave_dashboard_view, name='dashboard'),
    path('apply/', views.apply_leave_view, name='apply'),
    path('approve/<int:application_id>/', views.approve_leave_view, name='approve'),
]
