from decimal import Decimal
from .models import LeaveBalance, LeaveApplication
from apps.audit.services import AuditService

class LeaveService:
    @staticmethod
    def submit_application(employee, leave_type, start_date, end_date, reason, contact_details='', session='FULL_DAY', attachment=None):
        # Calculate days
        days = Decimal((end_date - start_date).days + 1)
        if session != 'FULL_DAY':
            days = Decimal('0.5')
            
        app = LeaveApplication.objects.create(
            organization=employee.organization,
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            number_of_days=days,
            session=session,
            reason=reason,
            contact_details=contact_details,
            attachment=attachment,
            status='PENDING'
        )
        
        # update pending balance
        year = start_date.year
        bal, _ = LeaveBalance.objects.get_or_create(employee=employee, leave_type=leave_type, year=year, organization=employee.organization)
        bal.pending_days += days
        bal.save()
        
        return app

    @staticmethod
    def approve_application(application, reviewer):
        application.status = 'APPROVED'
        application.reviewed_by = reviewer
        application.save()
        
        # deduct from balance
        year = application.start_date.year
        bal, _ = LeaveBalance.objects.get_or_create(
            employee=application.employee,
            leave_type=application.leave_type,
            year=year,
            organization=application.organization
        )
        bal.pending_days = max(Decimal('0.0'), bal.pending_days - application.number_of_days)
        bal.used_days += application.number_of_days
        bal.save()
        
        return application
