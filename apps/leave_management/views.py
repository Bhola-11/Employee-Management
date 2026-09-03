from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import LeaveType, LeaveBalance, LeaveApplication
from .forms import LeaveTypeForm, LeaveApplicationForm
from .services import LeaveService

@login_required
def leave_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    balances = []
    my_applications = []
    if employee:
        balances = LeaveBalance.objects.filter(employee=employee, year=2026).select_related('leave_type')
        my_applications = LeaveApplication.objects.filter(employee=employee).order_by('-created_at')[:10]
        
    pending_approvals = LeaveApplication.objects.filter(organization=org, status='PENDING').select_related('employee', 'leave_type')[:15]
    
    return render(request, 'leave_management/dashboard.html', {
        'balances': balances,
        'my_applications': my_applications,
        'pending_approvals': pending_approvals,
        'employee': employee
    })

@login_required
def apply_leave_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "No employee profile found for user.")
        return redirect('leave_management:dashboard')
        
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            app = form.save(commit=False)
            app.organization = org
            app.employee = employee
            days = (app.end_date - app.start_date).days + 1
            app.number_of_days = days if app.session == 'FULL_DAY' else 0.5
            app.save()
            messages.success(request, f"Leave application for {app.number_of_days} days submitted.")
            return redirect('leave_management:dashboard')
    else:
        form = LeaveApplicationForm(organization=org)
    return render(request, 'leave_management/apply.html', {'form': form})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'DEPT_MANAGER', 'TEAM_LEAD')
def approve_leave_view(request, application_id):
    org = request.tenant_org
    app = get_object_or_404(LeaveApplication, id=application_id, organization=org)
    reviewer = getattr(request.user, 'employee_profile', None)
    LeaveService.approve_application(app, reviewer)
    messages.success(request, f"Leave application for {app.employee.full_name} approved.")
    return redirect('leave_management:dashboard')
