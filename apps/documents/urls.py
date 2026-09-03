from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_vault_view, name='vault'),
    path('vault/', views.document_vault_view, name='vault_alt'),
    path('upload/', views.document_upload_view, name='upload'),
]
