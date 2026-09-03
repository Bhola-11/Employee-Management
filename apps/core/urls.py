from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('org/switch/<int:org_id>/', views.switch_organization_view, name='switch_org'),
    path('search/', views.global_search_view, name='global_search'),
    path('theme/toggle/', views.toggle_theme_view, name='toggle_theme'),
]
