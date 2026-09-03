from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.travel_dashboard_view, name='dashboard'),
    path('dashboard/', views.travel_dashboard_view, name='dashboard_alt'),
    path('create/', views.travel_create_view, name='create'),
    path('<int:req_id>/approve/', views.travel_approve_view, name='approve'),
]
