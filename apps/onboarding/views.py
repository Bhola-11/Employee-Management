from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.accounts.permissions import role_required
from .models import EmployeeOnboarding, OnboardingTask, EmployeeOffboarding, OffboardingClearance
from .forms import EmployeeOnboardingForm, OnboardingTaskUpdateForm, EmployeeOffboardingForm, OffboardingClearanceForm
from .services import OnboardingService, OffboardingService

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE')
def onboarding_dashboard_view(request):
    org = request.tenant_org
    onboardings = EmployeeOnboarding.objects.filter(employee__organization=org).select_related('employee', 'template', 'buddy')
    offboardings = EmployeeOffboarding.objects.filter(employee__organization=org).select_related('employee', 'handover_to')
    
    in_progress_count = onboardings.filter(status='IN_PROGRESS').count()
    completed_count = onboardings.filter(status='COMPLETED').count()
    active_exits = offboardings.exclude(status='COMPLETED').count()
    
    return render(request, 'onboarding/dashboard.html', {
        'onboardings': onboardings,
        'offboardings': offboardings,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'active_exits': active_exits
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE')
def onboarding_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = EmployeeOnboardingForm(request.POST, organization=org)
        if form.is_valid():
            onboarding = form.save()
            OnboardingService.instantiate_onboarding(onboarding, request.user)
            messages.success(request, f"Onboarding workflow created for {onboarding.employee.full_name}")
            return redirect('onboarding:detail', onboarding.id)
    else:
        form = EmployeeOnboardingForm(organization=org)
    return render(request, 'onboarding/onboarding_form.html', {'form': form, 'title': 'Initiate Employee Onboarding'})

@login_required
def onboarding_detail_view(request, onboarding_id):
    org = request.tenant_org
    onboarding = get_object_or_404(EmployeeOnboarding, id=onboarding_id, employee__organization=org)
    tasks = onboarding.tasks.all()
    return render(request, 'onboarding/detail.html', {'onboarding': onboarding, 'tasks': tasks})

@login_required
def task_toggle_view(request, task_id):
    org = request.tenant_org
    task = get_object_or_404(OnboardingTask, id=task_id, onboarding__employee__organization=org)
    if task.status == 'COMPLETED':
        task.status = 'PENDING'
        task.completed_at = None
    else:
        task.status = 'COMPLETED'
        task.completed_at = timezone.now()
    task.save()
    task.onboarding.calculate_progress()
    messages.success(request, f"Task '{task.title}' updated.")
    return redirect('onboarding:detail', task.onboarding.id)

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'HR_EXECUTIVE')
def offboarding_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = EmployeeOffboardingForm(request.POST, organization=org)
        if form.is_valid():
            offboarding = form.save()
            OffboardingService.initiate_offboarding(offboarding, request.user)
            messages.success(request, f"Offboarding clearance started for {offboarding.employee.full_name}")
            return redirect('onboarding:offboarding_detail', offboarding.id)
    else:
        form = EmployeeOffboardingForm(organization=org)
    return render(request, 'onboarding/offboarding_form.html', {'form': form, 'title': 'Initiate Employee Offboarding'})

@login_required
def offboarding_detail_view(request, offboarding_id):
    org = request.tenant_org
    offboarding = get_object_or_404(EmployeeOffboarding, id=offboarding_id, employee__organization=org)
    clearances = offboarding.clearances.all()
    return render(request, 'onboarding/offboarding_detail.html', {'offboarding': offboarding, 'clearances': clearances})
