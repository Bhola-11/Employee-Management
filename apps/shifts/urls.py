from django.urls import path
from . import views

app_name = 'shifts'

urlpatterns = [
    path('roster/', views.roster_view, name='roster'),
    path('types/create/', views.shift_type_create_view, name='type_create'),
    path('assign/', views.roster_assign_view, name='assign'),
]
