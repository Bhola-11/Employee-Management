from django.conf import settings

def worksphere_context(request):
    user = request.user
    context = {
        'APP_NAME': getattr(settings, 'WORKSPHERE_APP_NAME', 'WorkSphere'),
        'TAGLINE': getattr(settings, 'WORKSPHERE_TAGLINE', 'One Platform for Every Workforce'),
        'APP_VERSION': getattr(settings, 'WORKSPHERE_VERSION', '1.0.0'),
        'current_organization': getattr(request, 'organization', None),
        'user_roles': [],
        'user_role_names': [],
        'primary_role': None,
        'active_role_code': None,
        'is_org_admin': False,
        'is_super_admin': False,
    }

    if user.is_authenticated:
        context['is_super_admin'] = user.is_superuser or user.is_super_admin
        context['is_org_admin'] = user.is_org_admin
        
        assignments = list(user.role_assignments.select_related('role').all())
        context['user_roles'] = [a.role for a in assignments]
        context['user_role_names'] = [a.role.name for a in assignments]
        
        active_role = getattr(user, 'active_role', None)
        if active_role:
            context['primary_role'] = active_role.name
            context['active_role_code'] = active_role.code
        elif assignments:
            context['primary_role'] = assignments[0].role.name
            context['active_role_code'] = assignments[0].role.code
        elif user.is_superuser:
            context['primary_role'] = 'Super Admin'
            context['active_role_code'] = 'SUPER_ADMIN'
        else:
            context['primary_role'] = 'Employee'
            context['active_role_code'] = 'EMPLOYEE'

        if hasattr(user, 'employee_profile'):
            context['employee_profile'] = user.employee_profile

    return context
