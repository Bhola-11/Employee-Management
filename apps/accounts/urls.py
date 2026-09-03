from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('roles/', views.roles_matrix_view, name='roles_matrix'),
    path('roles-matrix/', views.roles_matrix_view, name='roles_matrix_alt'),
    path('switch-role/<str:role_code>/', views.switch_active_role_view, name='switch_role'),
]
