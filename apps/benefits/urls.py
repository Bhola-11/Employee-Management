from django.urls import path
from . import views

app_name = 'benefits'

urlpatterns = [
    path('dashboard/', views.benefits_dashboard_view, name='dashboard'),
    path('enroll/', views.enroll_benefit_view, name='enroll'),
]
