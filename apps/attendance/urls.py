from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_dashboard_view, name='dashboard'),
    path('dashboard/', views.attendance_dashboard_view, name='dashboard_alt'),
    path('clock-in/', views.clock_in_view, name='clock_in'),
    path('clock-out/', views.clock_out_view, name='clock_out'),
    path('regularization/request/', views.regularization_create_view, name='regularization_request_general'),
    path('regularization/<int:attendance_id>/request/', views.regularization_create_view, name='regularization_request'),
]
