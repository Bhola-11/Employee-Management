from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.assets_dashboard_view, name='dashboard'),
    path('dashboard/', views.assets_dashboard_view, name='dashboard_alt'),
    path('create/', views.asset_create_view, name='create'),
]
