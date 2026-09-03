from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_directory_view, name='directory'),
    path('add/', views.employee_create_view, name='create'),
    path('me/', views.my_profile_view, name='my_profile'),
    path('org-chart/', views.org_chart_view, name='org_chart'),
    path('<uuid:pk>/', views.employee_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.employee_edit_view, name='edit'),
    path('<uuid:pk>/lifecycle/', views.employee_lifecycle_transition_view, name='lifecycle'),
]
