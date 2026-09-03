from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import AppraisalCycle, GoalObjective, EmployeeAppraisal
from .forms import GoalObjectiveForm, SelfAppraisalForm, ManagerAppraisalForm

@login_required
def performance_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    my_goals = []
    my_appraisals = []
    if employee:
        my_goals = GoalObjective.objects.filter(employee=employee).order_by('-target_date')
        my_appraisals = EmployeeAppraisal.objects.filter(employee=employee).select_related('cycle')
        
    cycles = AppraisalCycle.objects.filter(organization=org)
    return render(request, 'performance/dashboard.html', {
        'my_goals': my_goals,
        'my_appraisals': my_appraisals,
        'cycles': cycles,
        'employee': employee
    })

@login_required
def goal_create_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required to set OKRs.")
        return redirect('performance:dashboard')
        
    if request.method == 'POST':
        form = GoalObjectiveForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.organization = org
            goal.employee = employee
            goal.save()
            messages.success(request, f"OKR Goal '{goal.title}' established.")
            return redirect('performance:dashboard')
    else:
        form = GoalObjectiveForm()
    return render(request, 'performance/goal_form.html', {'form': form, 'title': 'Create OKR Goal Objective'})

@login_required
def self_appraisal_view(request, appraisal_id):
    org = request.tenant_org
    appraisal = get_object_or_404(EmployeeAppraisal, id=appraisal_id, cycle__organization=org)
    if request.method == 'POST':
        form = SelfAppraisalForm(request.POST, instance=appraisal)
        if form.is_valid():
            app = form.save(commit=False)
            app.status = 'SUBMITTED_SELF'
            app.save()
            messages.success(request, "Self appraisal submitted to your reporting manager.")
            return redirect('performance:dashboard')
    else:
        form = SelfAppraisalForm(instance=appraisal)
    return render(request, 'performance/appraisal_form.html', {'form': form, 'appraisal': appraisal, 'title': 'Submit Self Appraisal'})
