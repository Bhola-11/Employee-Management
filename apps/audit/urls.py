from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_log_list_view, name='log_list'),
    path('<uuid:pk>/', views.audit_log_detail_view, name='log_detail'),
]
