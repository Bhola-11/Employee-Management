from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.learning_dashboard_view, name='dashboard'),
    path('dashboard/', views.learning_dashboard_view, name='dashboard_alt'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course_view, name='enroll_course'),
]
