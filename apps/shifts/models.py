from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class ShiftType(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='shift_types')
    name = models.CharField(max_length=100) # General Morning, Evening, Night Shift, Weekend Rotational
    code = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    grace_period_minutes = models.PositiveIntegerField(default=15)
    break_duration_minutes = models.PositiveIntegerField(default=60)
    is_night_shift = models.BooleanField(default=False)
    half_day_minimum_hours = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('4.50'))
    full_day_minimum_hours = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('8.00'))

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class ShiftRoster(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='shift_rosters')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='shift_rosters')
    shift_type = models.ForeignKey(ShiftType, on_delete=models.CASCADE, related_name='roster_entries')
    date = models.DateField(db_index=True)
    is_weekly_off = models.BooleanField(default=False)
    assigned_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='rostered_assignments')

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee__first_name']

    def __str__(self):
        off = " [Weekly Off]" if self.is_weekly_off else ""
        return f"{self.employee.full_name}: {self.shift_type.name} on {self.date}{off}"


class ShiftSwapRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING_PEER', 'Awaiting Peer Acceptance'),
        ('PENDING_MANAGER', 'Awaiting Manager Approval'),
        ('APPROVED', 'Approved & Rosters Swapped'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled by Requester'),
    )
    requesting_employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='outbound_swap_requests')
    requested_employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='inbound_swap_requests')
    
    requesting_roster = models.ForeignKey(ShiftRoster, on_delete=models.CASCADE, related_name='outbound_swaps')
    requested_roster = models.ForeignKey(ShiftRoster, on_delete=models.CASCADE, related_name='inbound_swaps')
    
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_PEER')
    
    peer_responded_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_shift_swaps')
    manager_action_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Swap Request: {self.requesting_employee.full_name} <-> {self.requested_employee.full_name} [{self.status}]"
