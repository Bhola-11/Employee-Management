from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Role, UserRoleAssignment, UserSessionLog, Permission, RolePermission
from .forms import UserLoginForm, UserProfileForm, UserCreateForm, UserRoleAssignmentForm
from .services import AuthService, RBACService
from apps.core.utils import paginate_queryset

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            AuthService.log_user_session(request, user)
            
            # Set default active organization in session
            if user.organization:
                request.session['active_organization_id'] = user.organization.id

            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            next_url = request.GET.get('next') or 'core:dashboard'
            return redirect(next_url)
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    AuthService.close_user_session(request, request.user)
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)

    roles = user.role_assignments.select_related('role', 'organization').all()
    sessions = UserSessionLog.objects.filter(user=user)[:5]

    return render(request, 'accounts/profile.html', {
        'form': form,
        'user': user,
        'roles': roles,
        'sessions': sessions
    })

@login_required
def switch_active_role_view(request, role_code):
    "Allows multi-role users or admins to dynamically switch active persona for testing/operations."
    user = request.user
    try:
        role = Role.objects.get(code=role_code)
        if user.is_superuser or user.has_role(role_code):
            user.active_role = role
            user.save(update_fields=['active_role'])
            messages.success(request, f'Switched active operational role to: {role.name}')
    except Role.DoesNotExist:
        messages.error(request, 'Invalid role selected.')
    return redirect(request.META.get('HTTP_REFERER', 'core:dashboard'))

@login_required
def user_list_view(request):
    org = request.organization
    users = User.objects.filter(organization=org).prefetch_related('role_assignments__role')
    page_obj = paginate_queryset(request, users, 15)
    return render(request, 'accounts/user_list.html', {'page_obj': page_obj, 'users': page_obj.object_list})

@login_required
def user_create_view(request):
    org = request.organization
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = org
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Assign selected role
            role = form.cleaned_data['role']
            RBACService.assign_role_to_user(user, role.code, org, is_primary=True, assigned_by=request.user)
            
            messages.success(request, f'User {user.email} created with role {role.name}.')
            return redirect('accounts:user_list')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create New User'})

@login_required
def roles_and_permissions_view(request):
    roles = Role.objects.all().prefetch_related('role_permissions__permission')
    permissions = Permission.objects.all()
    return render(request, 'accounts/roles_matrix.html', {'roles': roles, 'permissions': permissions})
