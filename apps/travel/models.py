from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class TravelRequisition(TimeStampedModel):
    PURPOSE_CHOICES = (
        ('CLIENT_MEETING', 'Client Onsite Meeting / Pitch'),
        ('CONFERENCE', 'Industry Conference / Summit'),
        ('INTERNAL_TRANSFER', 'Internal Branch Audit / Transfer'),
        ('TRAINING', 'Technical Training Workshop'),
    )
    STATUS_CHOICES = (
        ('PENDING_MANAGER', 'Pending Manager Approval'),
        ('PENDING_TRAVEL_DESK', 'Pending Travel Desk Booking'),
        ('BOOKED', 'Itinerary Booked & Confirmed'),
        ('COMPLETED', 'Travel Completed - Awaiting Settlement'),
        ('SETTLED', 'Expenses Reconciled & Closed'),
        ('REJECTED', 'Rejected'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='travel_requisitions')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='travel_requisitions')
    requisition_number = models.CharField(max_length=50, unique=True)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default='CLIENT_MEETING')
    description = models.TextField()
    
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField()
    
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    advance_amount_requested = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='PENDING_MANAGER')
    
    approved_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_travels')
    booking_reference = models.CharField(max_length=100, blank=True)
    itinerary_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-departure_date']

    def __str__(self):
        return f"Travel #{self.requisition_number}: {self.origin_city} -> {self.destination_city} ({self.employee.full_name})"
