from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.org_detail_view, name='index'),
    path('profile/', views.org_detail_view, name='detail'),
    path('settings/', views.org_settings_edit_view, name='settings'),
    
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/add/', views.department_create_view, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit_view, name='department_edit'),

    path('branches/', views.branch_list_view, name='branch_list'),
    path('branches/add/', views.branch_create_view, name='branch_create'),
    path('branches/<int:pk>/edit/', views.branch_edit_view, name='branch_edit'),

    path('designations/', views.designation_list_view, name='designation_list'),
    path('designations/add/', views.designation_create_view, name='designation_create'),
    path('designations/<int:pk>/edit/', views.designation_edit_view, name='designation_edit'),

    path('structure-config/', views.job_level_list_view, name='structure_config'),
]
