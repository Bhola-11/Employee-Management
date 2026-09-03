from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import ShiftType, ShiftRoster, ShiftSwapRequest
from .forms import ShiftTypeForm, ShiftRosterForm

@login_required
def roster_view(request):
    org = request.tenant_org
    shift_types = ShiftType.objects.filter(organization=org)
    rosters = ShiftRoster.objects.filter(organization=org).select_related('employee', 'shift_type')[:30]
    return render(request, 'shifts/roster.html', {
        'shift_types': shift_types,
        'rosters': rosters
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'TEAM_LEAD')
def shift_type_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = ShiftTypeForm(request.POST)
        if form.is_valid():
            st = form.save(commit=False)
            st.organization = org
            st.save()
            messages.success(request, f"Shift Type '{st.name}' created.")
            return redirect('shifts:roster')
    else:
        form = ShiftTypeForm()
    return render(request, 'shifts/shift_type_form.html', {'form': form, 'title': 'Create Shift Pattern'})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'TEAM_LEAD')
def roster_assign_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = ShiftRosterForm(request.POST, organization=org)
        if form.is_valid():
            rost = form.save(commit=False)
            rost.organization = org
            rost.assigned_by = getattr(request.user, 'employee_profile', None)
            rost.save()
            messages.success(request, f"Rostered {rost.employee.full_name} on {rost.date}.")
            return redirect('shifts:roster')
    else:
        form = ShiftRosterForm(organization=org)
    return render(request, 'shifts/roster_form.html', {'form': form, 'title': 'Assign Shift Roster'})
