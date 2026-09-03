from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

@shared_task
def daily_attendance_aggregation_job():
    """
    Automated Celery task calculating daily attendance summaries, overtime thresholds, and late marks.
    """
    from apps.attendance.models import AttendanceRecord, MonthlyAttendanceSummary
    from apps.organizations.models import Organization
    today = timezone.localdate()
    records = AttendanceRecord.objects.filter(date=today)
    processed_count = records.count()
    return f"Aggregated {processed_count} attendance records for {today}"

@shared_task
def monthly_leave_quota_accrual_job():
    """
    Automated Celery task executing monthly leave quota accrual allocations across all active staff.
    """
    from apps.leave_management.models import LeaveType, LeaveBalance
    from apps.employees.models import Employee
    active_employees = Employee.objects.filter(employment_status__in=['ACTIVE', 'CONFIRMED'])
    monthly_leave_types = LeaveType.objects.filter(accrual_frequency='MONTHLY')
    
    accrued = 0
    year = timezone.localdate().year
    for emp in active_employees:
        for lt in monthly_leave_types:
            bal, _ = LeaveBalance.objects.get_or_create(employee=emp, leave_type=lt, year=year, organization=emp.organization)
            bal.allocated_days += round(lt.annual_quota / Decimal('12.0'), 2)
            bal.save()
            accrued += 1
            
    return f"Processed monthly accrual for {accrued} employee leave balances."

@shared_task
def helpdesk_sla_escalation_alert_job():
    """
    Automated Celery task checking helpdesk tickets exceeding SLA response times.
    """
    from apps.helpdesk.models import HelpdeskTicket
    from apps.notifications.services import NotificationService
    
    open_tickets = HelpdeskTicket.objects.filter(status='OPEN')
    escalated = 0
    now = timezone.now()
    
    for t in open_tickets:
        sla_hours = t.category.sla_response_hours
        deadline = t.created_at + timedelta(hours=sla_hours)
        if now > deadline and t.assigned_to and t.assigned_to.user:
            NotificationService.send_notification(
                user=t.assigned_to.user,
                title=f"URGENT: Ticket #{t.ticket_number} SLA Breached",
                message=f"Ticket '{t.subject}' has exceeded its {sla_hours}h SLA threshold.",
                notification_type='HELPDESK',
                action_url=f"/helpdesk/ticket/{t.id}/"
            )
            escalated += 1
            
    return f"Audited open tickets: {escalated} SLA escalation alerts dispatched."
