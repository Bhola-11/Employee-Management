from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, StatusModel

class TicketCategory(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='helpdesk_categories')
    name = models.CharField(max_length=100) # HR Operations, IT Support & Access, Payroll & Tax, Facilities & Badge
    code = models.CharField(max_length=50)
    sla_response_hours = models.PositiveIntegerField(default=24)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (SLA: {self.sla_response_hours}h)"


class HelpdeskTicket(TimeStampedModel):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent / Critical'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open / Unassigned'),
        ('IN_PROGRESS', 'In Progress / Assigned'),
        ('WAITING_EMPLOYEE', 'Waiting for Employee Response'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='helpdesk_tickets')
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=50, unique=True)
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='submitted_tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    resolution_notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to='ticket_attachments/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.ticket_number}: {self.subject} [{self.status}]"


class TicketComment(TimeStampedModel):
    ticket = models.ForeignKey(HelpdeskTicket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal_note = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on #{self.ticket.ticket_number} by {self.author.email}"
