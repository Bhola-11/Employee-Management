from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.accounts.permissions import role_required
from .models import BenefitPlan, EmployeeBenefitEnrollment
from .forms import BenefitPlanForm, EmployeeBenefitEnrollmentForm

@login_required
def benefits_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    plans = BenefitPlan.objects.filter(organization=org)
    my_enrollments = []
    if employee:
        my_enrollments = EmployeeBenefitEnrollment.objects.filter(employee=employee).select_related('plan')
        
    return render(request, 'benefits/dashboard.html', {
        'plans': plans,
        'my_enrollments': my_enrollments,
        'employee': employee
    })

@login_required
def enroll_benefit_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "No employee profile linked to user.")
        return redirect('benefits:dashboard')
        
    if request.method == 'POST':
        form = EmployeeBenefitEnrollmentForm(request.POST, organization=org)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.employee = employee
            enrollment.enrolled_date = timezone.localdate()
            enrollment.status = 'ACTIVE'
            enrollment.save()
            messages.success(request, f"Enrolled into {enrollment.plan.name} successfully.")
            return redirect('benefits:dashboard')
    else:
        form = EmployeeBenefitEnrollmentForm(organization=org)
    return render(request, 'benefits/enroll_form.html', {'form': form, 'title': 'Enroll in Benefit Plan'})
