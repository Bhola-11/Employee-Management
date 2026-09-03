from django.urls import path
from . import views

app_name = 'benefits'

urlpatterns = [
    path('', views.benefits_dashboard_view, name='dashboard'),
    path('dashboard/', views.benefits_dashboard_view, name='dashboard_alt'),
    path('enroll/', views.enroll_benefit_view, name='enroll'),
    path('enroll/<int:plan_id>/', views.enroll_benefit_view, name='enroll_plan'),
]
