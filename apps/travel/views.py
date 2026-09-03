import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import TravelRequisition
from .forms import TravelRequisitionForm

@login_required
def travel_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    my_travels = []
    if employee:
        my_travels = TravelRequisition.objects.filter(employee=employee).order_by('-departure_date')
        
    all_travels = TravelRequisition.objects.filter(organization=org).select_related('employee')[:20]
    
    return render(request, 'travel/dashboard.html', {
        'my_travels': my_travels,
        'all_travels': all_travels,
        'employee': employee
    })

@login_required
def travel_create_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required to file travel request.")
        return redirect('travel:dashboard')
        
    if request.method == 'POST':
        form = TravelRequisitionForm(request.POST)
        if form.is_valid():
            trav = form.save(commit=False)
            trav.organization = org
            trav.employee = employee
            trav.requisition_number = f"TRV-{uuid.uuid4().hex[:6].upper()}"
            trav.save()
            messages.success(request, f"Travel Request #{trav.requisition_number} submitted.")
            return redirect('travel:dashboard')
    else:
        form = TravelRequisitionForm()
    return render(request, 'travel/travel_form.html', {'form': form, 'title': 'Request Business Travel'})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'FINANCE_MANAGER', 'TEAM_LEAD')
def travel_approve_view(request, requisition_id):
    org = request.tenant_org
    trav = get_object_or_404(TravelRequisition, id=requisition_id, organization=org)
    trav.status = 'BOOKED'
    trav.approved_by = getattr(request.user, 'employee_profile', None)
    trav.booking_reference = f"PNR-{uuid.uuid4().hex[:6].upper()}"
    trav.save()
    messages.success(request, f"Travel Request #{trav.requisition_number} approved and booked (Ref: {trav.booking_reference}).")
    return redirect('travel:dashboard')
