from django.urls import path
from . import views

app_name = 'onboarding'

urlpatterns = [
    path('dashboard/', views.onboarding_dashboard_view, name='dashboard'),
    path('create/', views.onboarding_create_view, name='create'),
    path('<int:onboarding_id>/', views.onboarding_detail_view, name='detail'),
    path('task/<int:task_id>/toggle/', views.task_toggle_view, name='task_toggle'),
    path('offboarding/create/', views.offboarding_create_view, name='offboarding_create'),
    path('offboarding/<int:offboarding_id>/', views.offboarding_detail_view, name='offboarding_detail'),
]
