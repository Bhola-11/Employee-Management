from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('dashboard/', views.assets_dashboard_view, name='dashboard'),
    path('create/', views.asset_create_view, name='create'),
]
