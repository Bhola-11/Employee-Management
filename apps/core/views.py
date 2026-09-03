from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q

@login_required
def dashboard_view(request):
    org = request.organization
    context = {
        'page_title': 'Enterprise Workforce Dashboard',
        'total_employees': 0,
        'active_employees': 0,
        'on_leave_today': 0,
        'present_today': 0,
        'open_jobs': 0,
        'pending_approvals': 0,
        'departments_count': 0,
        'recent_activities': [],
        'department_distribution': [],
        'attendance_rate': 94.5,
    }

    if org:
        from apps.employees.models import Employee
        from apps.organizations.models import Department
        from apps.audit.models import ActivityLog

        emp_qs = Employee.objects.filter(organization=org)
        context['total_employees'] = emp_qs.count()
        context['active_employees'] = emp_qs.filter(employment_status__in=['ACTIVE', 'CONFIRMED', 'PROBATION']).count()
        context['departments_count'] = Department.objects.filter(organization=org, is_active=True).count()
        
        dept_data = Department.objects.filter(organization=org, is_active=True).annotate(
            emp_count=Count('employees')
        ).values('name', 'emp_count')[:6]
        context['department_distribution'] = list(dept_data)

        context['recent_activities'] = ActivityLog.objects.filter(organization=org)[:8]

    return render(request, 'dashboard/index.html', context)

@login_required
def switch_organization_view(request, org_id):
    from apps.organizations.models import Organization
    try:
        org = Organization.objects.get(id=org_id, is_active=True)
        if request.user.is_superuser or request.user.organization_id == org.id:
            request.session['active_organization_id'] = org.id
    except Organization.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', 'core:dashboard'))

@login_required
def global_search_view(request):
    query = request.GET.get('q', '').strip()
    org = request.organization
    results = {'employees': [], 'departments': []}
    
    if query and org:
        from apps.employees.models import Employee
        from apps.organizations.models import Department

        emps = Employee.objects.filter(
            organization=org
        ).filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(work_email__icontains=query)
        )[:10]

        for e in emps:
            results['employees'].append({
                'id': e.id,
                'name': f'{e.first_name} {e.last_name}',
                'employee_id': e.employee_id,
                'designation': e.designation.title if e.designation else '',
                'department': e.department.name if e.department else '',
            })

        depts = Department.objects.filter(
            organization=org,
            name__icontains=query
        )[:5]
        for d in depts:
            results['departments'].append({
                'id': d.id,
                'name': d.name,
                'code': d.code,
            })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(results)
    return render(request, 'dashboard/search_results.html', {'query': query, 'results': results})

@login_required
def toggle_theme_view(request):
    dark_mode = request.session.get('dark_mode', False)
    request.session['dark_mode'] = not dark_mode
    if hasattr(request.user, 'dark_mode'):
        request.user.dark_mode = not dark_mode
        request.user.save(update_fields=['dark_mode'])
    return JsonResponse({'dark_mode': not dark_mode})
