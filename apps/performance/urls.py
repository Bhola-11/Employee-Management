from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    path('', views.performance_dashboard_view, name='dashboard'),
    path('dashboard/', views.performance_dashboard_view, name='dashboard_alt'),
    path('goals/create/', views.goal_create_view, name='goal_create'),
    path('appraisal/<int:appraisal_id>/self/', views.self_appraisal_view, name='self_appraisal'),
]
