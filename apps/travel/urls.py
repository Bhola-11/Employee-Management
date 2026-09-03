from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('dashboard/', views.travel_dashboard_view, name='dashboard'),
    path('create/', views.travel_create_view, name='create'),
    path('<int:requisition_id>/approve/', views.travel_approve_view, name='approve'),
]
