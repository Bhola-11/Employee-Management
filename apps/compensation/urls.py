from django.urls import path
from . import views

app_name = 'compensation'

urlpatterns = [
    path('', views.compensation_dashboard_view, name='dashboard'),
    path('dashboard/', views.compensation_dashboard_view, name='dashboard_alt'),
    path('bands/create/', views.salary_band_create_view, name='band_create'),
]
