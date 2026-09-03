from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.core.models import TimeStampedModel

class AttendanceRecord(TimeStampedModel):
    STATUS_CHOICES = (
        ('PRESENT', 'Present (Full Day)'),
        ('HALF_DAY', 'Half Day'),
        ('ABSENT', 'Absent'),
        ('ON_LEAVE', 'Approved Leave'),
        ('HOLIDAY', 'Company Holiday'),
        ('WEEKLY_OFF', 'Weekly Off'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='attendance_records')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    
    total_work_hours = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    break_hours = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'))
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')
    is_late_entry = models.BooleanField(default=False)
    is_early_exit = models.BooleanField(default=False)
    is_regularized = models.BooleanField(default=False)
    
    clock_in_ip = models.GenericIPAddressField(null=True, blank=True)
    clock_out_ip = models.GenericIPAddressField(null=True, blank=True)
    clock_in_device = models.CharField(max_length=255, blank=True)
    clock_out_device = models.CharField(max_length=255, blank=True)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee__first_name']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.status})"


class AttendanceRegularization(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved & Record Updated'),
        ('REJECTED', 'Rejected'),
    )
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='regularizations')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='regularization_requests')
    requested_clock_in = models.TimeField()
    requested_clock_out = models.TimeField()
    reason = models.CharField(max_length=255)
    detailed_explanation = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_regularizations')
    approved_at = models.DateTimeField(null=True, blank=True)
    approver_comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Regularization for {self.employee.full_name} on {self.attendance_record.date}"


class MonthlyAttendanceSummary(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='monthly_attendance_summaries')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='monthly_attendance_summaries')
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField() # 1-12
    
    total_working_days = models.PositiveSmallIntegerField(default=22)
    present_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    absent_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    leave_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    holidays = models.PositiveSmallIntegerField(default=0)
    weekly_offs = models.PositiveSmallIntegerField(default=8)
    late_entries_count = models.PositiveSmallIntegerField(default=0)
    total_overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    is_locked_for_payroll = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.full_name} Summary ({self.year}-{self.month:02d})"
