from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('dashboard/', views.expenses_dashboard_view, name='dashboard'),
    path('claims/create/', views.claim_create_view, name='claim_create'),
    path('claims/<int:claim_id>/', views.claim_detail_view, name='claim_detail'),
    path('claims/<int:claim_id>/approve/', views.approve_claim_view, name='approve_claim'),
]
