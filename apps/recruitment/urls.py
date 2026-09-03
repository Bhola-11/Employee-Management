from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    path('dashboard/', views.recruitment_dashboard_view, name='dashboard'),
    path('requisitions/', views.requisition_list_view, name='requisition_list'),
    path('requisitions/create/', views.requisition_create_view, name='requisition_create'),
    path('requisitions/<int:requisition_id>/', views.requisition_detail_view, name='requisition_detail'),
    path('candidates/', views.candidate_list_view, name='candidate_list'),
    path('candidates/create/', views.candidate_create_view, name='candidate_create'),
    path('candidates/<int:candidate_id>/', views.candidate_detail_view, name='candidate_detail'),
]
