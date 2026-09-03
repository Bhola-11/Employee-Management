from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('', views.payroll_dashboard_view, name='dashboard'),
    path('dashboard/', views.payroll_dashboard_view, name='dashboard_alt'),
    path('run/create/', views.payroll_run_create_view, name='run_create'),
    path('run/<int:run_id>/', views.payroll_run_detail_view, name='run_detail'),
    path('runs/<int:run_id>/', views.payroll_run_detail_view, name='payroll_run_detail'),
    path('payslip/<int:payslip_id>/', views.payslip_detail_view, name='payslip_detail'),
]
