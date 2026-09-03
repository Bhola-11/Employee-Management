from datetime import date, datetime
from django.utils import timezone
from decimal import Decimal
from .models import AttendanceRecord

class AttendanceService:
    @staticmethod
    def punch_in(employee, ip_address='127.0.0.1'):
        today = timezone.localdate()
        rec, created = AttendanceRecord.objects.get_or_create(
            organization=employee.organization,
            employee=employee,
            date=today,
            defaults={'status': 'PRESENT'}
        )
        if not rec.clock_in:
            rec.clock_in = timezone.now()
            rec.clock_in_ip = ip_address
            # Late check (e.g. after 09:30 AM)
            if rec.clock_in.hour >= 10:
                rec.is_late_entry = True
            rec.save()
        return rec

    @staticmethod
    def punch_out(employee, ip_address='127.0.0.1'):
        today = timezone.localdate()
        try:
            rec = AttendanceRecord.objects.get(employee=employee, date=today)
            rec.clock_out = timezone.now()
            rec.clock_out_ip = ip_address
            
            # calculate hours
            if rec.clock_in:
                diff = rec.clock_out - rec.clock_in
                total_hours = Decimal(diff.total_seconds() / 3600.0)
                rec.total_work_hours = round(total_hours, 2)
                if rec.total_work_hours < Decimal('4.5'):
                    rec.status = 'HALF_DAY'
                elif rec.total_work_hours >= Decimal('9.0'):
                    rec.overtime_hours = round(rec.total_work_hours - Decimal('8.5'), 2)
            rec.save()
            return rec
        except AttendanceRecord.DoesNotExist:
            return None
