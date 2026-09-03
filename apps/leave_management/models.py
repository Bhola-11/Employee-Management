from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class LeaveType(TimeStampedModel, StatusModel):
    ACCRUAL_FREQUENCY_CHOICES = (
        ('ANNUAL', 'Annual Upfront Grant'),
        ('MONTHLY', 'Monthly Accrual'),
        ('QUARTERLY', 'Quarterly Accrual'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='leave_types')
    name = models.CharField(max_length=100) # Paid Time Off, Sick Leave, Casual Leave, Maternity, Paternity, Bereavement
    code = models.CharField(max_length=50)
    annual_quota = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('12.0'))
    accrual_frequency = models.CharField(max_length=20, choices=ACCRUAL_FREQUENCY_CHOICES, default='ANNUAL')
    max_carry_forward_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('5.0'))
    is_encashable = models.BooleanField(default=False)
    is_unpaid = models.BooleanField(default=False)
    requires_attachment = models.BooleanField(default=False)
    color_hex = models.CharField(max_length=10, default='#2563eb')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class LeaveBalance(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='leave_balances')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='employee_balances')
    year = models.PositiveIntegerField()
    
    allocated_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    carried_forward_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    used_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    pending_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))

    class Meta:
        unique_together = ('employee', 'leave_type', 'year')
        ordering = ['leave_type__name']

    @property
    def total_available(self):
        return (self.allocated_days + self.carried_forward_days) - (self.used_days + self.pending_days)

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name} ({self.total_available} Left)"


class LeaveApplication(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    )
    SESSION_CHOICES = (
        ('FULL_DAY', 'Full Day'),
        ('FIRST_HALF', 'First Half'),
        ('SECOND_HALF', 'Second Half'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='leave_applications')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='applications')
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('1.0'))
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default='FULL_DAY')
    reason = models.TextField()
    contact_details = models.CharField(max_length=255, blank=True)
    attachment = models.FileField(upload_to='leave_attachments/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    manager_comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name}: {self.leave_type.name} ({self.start_date} to {self.end_date}) [{self.status}]"
