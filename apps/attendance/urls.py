from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('dashboard/', views.attendance_dashboard_view, name='dashboard'),
    path('clock-in/', views.clock_in_view, name='clock_in'),
    path('clock-out/', views.clock_out_view, name='clock_out'),
    path('regularize/<int:record_id>/', views.regularization_create_view, name='regularize'),
]
