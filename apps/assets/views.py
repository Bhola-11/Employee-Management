from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import Asset, AssetCategory
from .forms import AssetForm

@login_required
def assets_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    my_assets = []
    if employee:
        my_assets = Asset.objects.filter(assigned_to=employee).select_related('category')
        
    all_assets = Asset.objects.filter(organization=org).select_related('category', 'assigned_to')[:25]
    return render(request, 'assets/dashboard.html', {
        'my_assets': my_assets,
        'all_assets': all_assets,
        'employee': employee
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'IT_ASSET_MANAGER', 'HR_MANAGER')
def asset_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = AssetForm(request.POST, organization=org)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.organization = org
            asset.save()
            messages.success(request, f"Asset [{asset.asset_tag}] {asset.name} registered in inventory.")
            return redirect('assets:dashboard')
    else:
        form = AssetForm(organization=org)
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Register IT Hardware Asset'})
