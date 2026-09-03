import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import ExpenseClaim, ExpenseItem, ExpenseCategory
from .forms import ExpenseClaimForm, ExpenseItemForm

@login_required
def expenses_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    my_claims = []
    if employee:
        my_claims = ExpenseClaim.objects.filter(employee=employee).order_by('-created_at')[:10]
        
    pending_approvals = ExpenseClaim.objects.filter(organization=org, status='SUBMITTED').select_related('employee')[:15]
    
    return render(request, 'expenses/dashboard.html', {
        'my_claims': my_claims,
        'pending_approvals': pending_approvals,
        'employee': employee
    })

@login_required
def claim_create_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required to file expense claim.")
        return redirect('expenses:dashboard')
        
    if request.method == 'POST':
        form = ExpenseClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.organization = org
            claim.employee = employee
            claim.claim_number = f"EXP-{uuid.uuid4().hex[:6].upper()}"
            claim.save()
            messages.success(request, f"Expense Claim #{claim.claim_number} drafted. Add line items below.")
            return redirect('expenses:claim_detail', claim.id)
    else:
        form = ExpenseClaimForm()
    return render(request, 'expenses/claim_form.html', {'form': form, 'title': 'Create Expense Claim'})

@login_required
def claim_detail_view(request, claim_id):
    org = request.tenant_org
    claim = get_object_or_404(ExpenseClaim, id=claim_id, organization=org)
    items = claim.items.select_related('category').all()
    
    if request.method == 'POST':
        item_form = ExpenseItemForm(request.POST, request.FILES, organization=org)
        if item_form.is_valid():
            it = item_form.save(commit=False)
            it.claim = claim
            it.save()
            claim.calculate_total()
            messages.success(request, "Expense line item added.")
            return redirect('expenses:claim_detail', claim.id)
    else:
        item_form = ExpenseItemForm(organization=org)
        
    return render(request, 'expenses/claim_detail.html', {
        'claim': claim,
        'items': items,
        'item_form': item_form
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER', 'FINANCE_MANAGER', 'TEAM_LEAD')
def approve_claim_view(request, claim_id):
    org = request.tenant_org
    claim = get_object_or_404(ExpenseClaim, id=claim_id, organization=org)
    claim.status = 'PAID'
    claim.finance_auditor = getattr(request.user, 'employee_profile', None)
    claim.save()
    messages.success(request, f"Expense Claim #{claim.claim_number} approved and cleared for reimbursement.")
    return redirect('expenses:dashboard')
