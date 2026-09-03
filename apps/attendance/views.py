from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AttendanceRecord, AttendanceRegularization, MonthlyAttendanceSummary
from .forms import AttendanceRegularizationForm
from .services import AttendanceService

@login_required
def attendance_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    today = timezone.localdate()
    
    employee = getattr(user, 'employee_profile', None)
    today_punch = None
    if employee:
        today_punch = AttendanceRecord.objects.filter(employee=employee, date=today).first()
        
    recent_punches = AttendanceRecord.objects.filter(organization=org).select_related('employee', 'employee__department')[:15]
    
    return render(request, 'attendance/dashboard.html', {
        'today': today,
        'today_punch': today_punch,
        'recent_punches': recent_punches
    })

@login_required
def clock_in_view(request):
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Your user account is not linked to an employee profile.")
        return redirect('attendance:dashboard')
    
    rec = AttendanceService.punch_in(employee)
    messages.success(request, f"Punched in successfully at {timezone.localtime(rec.clock_in).strftime('%H:%M:%S')}")
    return redirect('attendance:dashboard')

@login_required
def clock_out_view(request):
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Your user account is not linked to an employee profile.")
        return redirect('attendance:dashboard')
    
    rec = AttendanceService.punch_out(employee)
    if rec:
        messages.success(request, f"Punched out successfully at {timezone.localtime(rec.clock_out).strftime('%H:%M:%S')}. Total Work: {rec.total_work_hours} hrs")
    else:
        messages.warning(request, "No clock-in record found for today.")
    return redirect('attendance:dashboard')

@login_required
def regularization_create_view(request, record_id):
    org = request.tenant_org
    rec = get_object_or_404(AttendanceRecord, id=record_id, organization=org)
    if request.method == 'POST':
        form = AttendanceRegularizationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.attendance_record = rec
            reg.employee = rec.employee
            reg.save()
            messages.success(request, "Attendance regularization request submitted.")
            return redirect('attendance:dashboard')
    else:
        form = AttendanceRegularizationForm()
    return render(request, 'attendance/regularization_form.html', {'form': form, 'record': rec})
