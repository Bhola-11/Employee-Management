from django.urls import path
from . import views

app_name = 'holidays'

urlpatterns = [
    path('', views.holiday_calendar_view, name='calendar'),
    path('create/', views.holiday_create_view, name='create'),
]
