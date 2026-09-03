from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import Holiday
from .forms import HolidayForm

@login_required
def holiday_calendar_view(request):
    org = request.tenant_org
    holidays = Holiday.objects.filter(organization=org).select_related('branch').order_by('date')
    return render(request, 'holidays/calendar.html', {'holidays': holidays})

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER')
def holiday_create_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = HolidayForm(request.POST, organization=org)
        if form.is_valid():
            h = form.save(commit=False)
            h.organization = org
            h.save()
            messages.success(request, f"Holiday '{h.name}' added to calendar.")
            return redirect('holidays:calendar')
    else:
        form = HolidayForm(organization=org)
    return render(request, 'holidays/form.html', {'form': form, 'title': 'Add Corporate Holiday'})
