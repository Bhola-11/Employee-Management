from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (
    Employee, EmergencyContact, EmployeeAddress, EmployeeEducation,
    EmployeePastExperience, EmployeeSkill, EmployeeBankDetail,
    EmployeeTaxInfo, EmployeeStatutoryDocument, EmployeeLifecycleTransition
)
from .forms import (
    EmployeeCreateForm, EmployeeUpdateForm, EmployeeBankDetailForm,
    EmployeeTaxInfoForm, EmergencyContactForm, EmployeeAddressForm,
    EmployeeLifecycleTransitionForm
)
from .services import EmployeeService
from apps.organizations.models import Department, Designation, Branch
from apps.core.utils import paginate_queryset

@login_required
def employee_directory_view(request):
    org = request.organization
    employees = Employee.objects.filter(organization=org).select_related(
        'department', 'designation', 'branch', 'job_level', 'employment_type'
    )

    # Search & Filters
    search_q = request.GET.get('search', '').strip()
    dept_id = request.GET.get('department')
    status = request.GET.get('status')
    branch_id = request.GET.get('branch')

    if search_q:
        employees = employees.filter(
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q) |
            Q(employee_id__icontains=search_q) |
            Q(work_email__icontains=search_q)
        )
    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if status:
        employees = employees.filter(employment_status=status)
    if branch_id:
        employees = employees.filter(branch_id=branch_id)

    page_obj = paginate_queryset(request, employees, 12)

    departments = Department.objects.filter(organization=org, is_active=True)
    branches = Branch.objects.filter(organization=org, is_active=True)
    
    return render(request, 'employees/directory.html', {
        'page_obj': page_obj,
        'employees': page_obj.object_list,
        'departments': departments,
        'branches': branches,
        'statuses': Employee.STATUS_CHOICES,
        'selected_dept': dept_id,
        'selected_status': status,
        'selected_branch': branch_id,
        'search_q': search_q,
    })

@login_required
def employee_detail_view(request, pk):
    org = request.organization
    employee = get_object_or_404(
        Employee.objects.select_related(
            'department', 'designation', 'branch', 'job_level',
            'employment_type', 'work_location', 'team', 'direct_manager'
        ),
        pk=pk,
        organization=org
    )
    
    contacts = employee.emergency_contacts.all()
    addresses = employee.addresses.all()
    educations = employee.educations.all()
    experiences = employee.past_experiences.all()
    skills = employee.skills.select_related('skill').all()
    documents = employee.statutory_documents.all()
    transitions = employee.lifecycle_transitions.select_related('changed_by')[:10]
    bank_detail = getattr(employee, 'bank_detail', None)
    tax_info = getattr(employee, 'tax_info', None)

    return render(request, 'employees/detail.html', {
        'employee': employee,
        'contacts': contacts,
        'addresses': addresses,
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
        'documents': documents,
        'transitions': transitions,
        'bank_detail': bank_detail,
        'tax_info': tax_info,
    })

@login_required
def employee_create_view(request):
    org = request.organization
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.organization = org
            if not emp.employee_id:
                emp.employee_id = EmployeeService.generate_next_employee_id(org)
            emp.save()
            messages.success(request, f'Employee {emp.full_name} created successfully with ID {emp.employee_id}.')
            return redirect('employees:detail', pk=emp.id)
    else:
        initial_id = EmployeeService.generate_next_employee_id(org) if org else 'WSP-00001'
        form = EmployeeCreateForm(organization=org, initial={'employee_id': initial_id})

    return render(request, 'employees/form.html', {'form': form, 'title': 'Create New Employee Record'})

@login_required
def employee_edit_view(request, pk):
    org = request.organization
    emp = get_object_or_404(Employee, pk=pk, organization=org)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=emp, organization=org)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee profile for {emp.full_name} updated successfully.')
            return redirect('employees:detail', pk=emp.id)
    else:
        form = EmployeeUpdateForm(instance=emp, organization=org)

    return render(request, 'employees/form.html', {'form': form, 'title': f'Edit Employee: {emp.full_name}'})

@login_required
def employee_lifecycle_transition_view(request, pk):
    org = request.organization
    emp = get_object_or_404(Employee, pk=pk, organization=org)
    if request.method == 'POST':
        form = EmployeeLifecycleTransitionForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['to_status']
            reason = form.cleaned_data['reason']
            remarks = form.cleaned_data['remarks']
            EmployeeService.transition_employee_status(emp, new_status, request.user, reason, remarks)
            messages.success(request, f'Status for {emp.full_name} updated to {new_status}.')
            return redirect('employees:detail', pk=emp.id)
    else:
        form = EmployeeLifecycleTransitionForm(initial={'to_status': emp.employment_status})

    return render(request, 'employees/lifecycle_modal.html', {'form': form, 'employee': emp})

@login_required
def org_chart_view(request):
    org = request.organization
    tree = EmployeeService.get_org_tree(org) if org else []
    return render(request, 'employees/org_chart.html', {'tree': tree})

@login_required
def my_profile_view(request):
    if hasattr(request.user, 'employee_profile'):
        return redirect('employees:detail', pk=request.user.employee_profile.id)
    messages.info(request, 'No linked employee profile found for your user account.')
    return redirect('accounts:profile')
