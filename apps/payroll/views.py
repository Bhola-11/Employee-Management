from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import PayrollRun, Payslip, EmployeeSalaryStructure
from .forms import PayrollRunForm
from .services import PayrollService

@login_required
def payroll_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    payroll_runs = PayrollRun.objects.filter(organization=org).order_by('-year', '-month')
    my_payslips = []
    if employee:
        my_payslips = Payslip.objects.filter(employee=employee).select_related('payroll_run')[:12]
        
    return render(request, 'payroll/dashboard.html', {
        'payroll_runs': payroll_runs,
        'my_payslips': my_payslips,
        'employee': employee
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'PAYROLL_MANAGER', 'FINANCE_MANAGER')
def payroll_run_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = PayrollRunForm(request.POST, organization=org)
        if form.is_valid():
            run = form.save(commit=False)
            run.organization = org
            run.save()
            PayrollService.process_payroll_run(run, request.user)
            messages.success(request, f"Payroll Run '{run.name}' processed successfully.")
            return redirect('payroll:run_detail', run.id)
    else:
        form = PayrollRunForm(organization=org)
    return render(request, 'payroll/run_form.html', {'form': form, 'title': 'Execute New Payroll Run'})

@login_required
def payroll_run_detail_view(request, run_id):
    org = request.tenant_org
    run = get_object_or_404(PayrollRun, id=run_id, organization=org)
    payslips = run.payslips.select_related('employee', 'employee__department').all()
    return render(request, 'payroll/run_detail.html', {'run': run, 'payslips': payslips})

@login_required
def payslip_detail_view(request, payslip_id):
    ps = get_object_or_404(Payslip, id=payslip_id)
    return render(request, 'payroll/payslip_view.html', {'payslip': ps})
