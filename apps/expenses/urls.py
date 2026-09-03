from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expenses_dashboard_view, name='dashboard'),
    path('dashboard/', views.expenses_dashboard_view, name='dashboard_alt'),
    path('claim/create/', views.claim_create_view, name='claim_create'),
    path('claim/<int:claim_id>/', views.claim_detail_view, name='claim_detail'),
    path('claim/<int:claim_id>/approve/', views.approve_claim_view, name='approve_claim'),
]
