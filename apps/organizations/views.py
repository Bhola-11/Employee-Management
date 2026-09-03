from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.core.utils import paginate_queryset
from .models import (
    Organization, Branch, Department, Team, Designation,
    JobLevel, EmploymentType, WorkLocation, ReportingHierarchy
)
from .forms import (
    OrganizationForm, BranchForm, DepartmentForm, TeamForm,
    DesignationForm, JobLevelForm, EmploymentTypeForm, WorkLocationForm
)
from .services import OrganizationService, HierarchyService

@login_required
def org_detail_view(request):
    org = request.organization
    if not org:
        messages.warning(request, 'Please configure or select an active organization.')
        return redirect('core:dashboard')
    
    overview = OrganizationService.get_organization_overview(org)
    return render(request, 'organizations/detail.html', {'overview': overview, 'org': org})

@login_required
def org_settings_edit_view(request):
    org = request.organization
    if not org:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization profile and settings updated successfully.')
            return redirect('organizations:detail')
    else:
        form = OrganizationForm(instance=org)
    return render(request, 'organizations/settings_form.html', {'form': form, 'org': org})

# --- Departments ---
@login_required
def department_list_view(request):
    org = request.organization
    departments = Department.objects.filter(organization=org).select_related('branch', 'parent_department', 'department_head')
    tree = HierarchyService.build_department_tree(org)
    return render(request, 'organizations/department_list.html', {
        'departments': departments,
        'department_tree': tree
    })

@login_required
def department_create_view(request):
    org = request.organization
    if request.method == 'POST':
        form = DepartmentForm(request.POST, organization=org)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.organization = org
            dept.save()
            messages.success(request, f'Department {dept.name} created successfully.')
            return redirect('organizations:department_list')
    else:
        form = DepartmentForm(organization=org)
    return render(request, 'organizations/department_form.html', {'form': form, 'title': 'Create New Department'})

@login_required
def department_edit_view(request, pk):
    org = request.organization
    dept = get_object_or_404(Department, pk=pk, organization=org)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept, organization=org)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department {dept.name} updated successfully.')
            return redirect('organizations:department_list')
    else:
        form = DepartmentForm(instance=dept, organization=org)
    return render(request, 'organizations/department_form.html', {'form': form, 'title': f'Edit Department: {dept.name}'})

# --- Branches ---
@login_required
def branch_list_view(request):
    org = request.organization
    branches = Branch.objects.filter(organization=org)
    return render(request, 'organizations/branch_list.html', {'branches': branches})

@login_required
def branch_create_view(request):
    org = request.organization
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.organization = org
            branch.save()
            messages.success(request, f'Branch {branch.name} created successfully.')
            return redirect('organizations:branch_list')
    else:
        form = BranchForm()
    return render(request, 'organizations/branch_form.html', {'form': form, 'title': 'Add New Branch / Location'})

@login_required
def branch_edit_view(request, pk):
    org = request.organization
    branch = get_object_or_404(Branch, pk=pk, organization=org)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, f'Branch {branch.name} updated successfully.')
            return redirect('organizations:branch_list')
    else:
        form = BranchForm(instance=branch)
    return render(request, 'organizations/branch_form.html', {'form': form, 'title': f'Edit Branch: {branch.name}'})

# --- Designations ---
@login_required
def designation_list_view(request):
    org = request.organization
    designations = Designation.objects.filter(organization=org).select_related('department', 'job_level')
    return render(request, 'organizations/designation_list.html', {'designations': designations})

@login_required
def designation_create_view(request):
    org = request.organization
    if request.method == 'POST':
        form = DesignationForm(request.POST, organization=org)
        if form.is_valid():
            desig = form.save(commit=False)
            desig.organization = org
            desig.save()
            messages.success(request, f'Designation {desig.title} created successfully.')
            return redirect('organizations:designation_list')
    else:
        form = DesignationForm(organization=org)
    return render(request, 'organizations/designation_form.html', {'form': form, 'title': 'Add Designation'})

@login_required
def designation_edit_view(request, pk):
    org = request.organization
    desig = get_object_or_404(Designation, pk=pk, organization=org)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=desig, organization=org)
        if form.is_valid():
            form.save()
            messages.success(request, f'Designation {desig.title} updated successfully.')
            return redirect('organizations:designation_list')
    else:
        form = DesignationForm(instance=desig, organization=org)
    return render(request, 'organizations/designation_form.html', {'form': form, 'title': f'Edit Designation: {desig.title}'})

# --- Job Levels & Types ---
@login_required
def job_level_list_view(request):
    org = request.organization
    levels = JobLevel.objects.filter(organization=org)
    types = EmploymentType.objects.filter(organization=org)
    locations = WorkLocation.objects.filter(organization=org).select_related('branch')
    return render(request, 'organizations/job_levels_and_types.html', {
        'levels': levels,
        'types': types,
        'locations': locations
    })
