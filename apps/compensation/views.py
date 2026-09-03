from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import SalaryBand, SalaryComponent
from .forms import SalaryBandForm, SalaryComponentForm

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'PAYROLL_MANAGER', 'FINANCE_MANAGER')
def compensation_dashboard_view(request):
    org = request.tenant_org
    bands = SalaryBand.objects.filter(organization=org).select_related('job_level')
    components = SalaryComponent.objects.filter(organization=org)
    return render(request, 'compensation/dashboard.html', {
        'bands': bands,
        'components': components
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'PAYROLL_MANAGER')
def salary_band_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = SalaryBandForm(request.POST, organization=org)
        if form.is_valid():
            band = form.save(commit=False)
            band.organization = org
            band.save()
            messages.success(request, f"Salary Band '{band.name}' established.")
            return redirect('compensation:dashboard')
    else:
        form = SalaryBandForm(organization=org)
    return render(request, 'compensation/band_form.html', {'form': form, 'title': 'Create Salary Band'})
