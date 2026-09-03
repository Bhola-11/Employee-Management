from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Notification(TimeStampedModel):
    TYPE_CHOICES = (
        ('INFO', 'System Information'),
        ('LEAVE', 'Leave Request & Approval'),
        ('ATTENDANCE', 'Attendance Alert'),
        ('PAYROLL', 'Payroll & Payslip Generated'),
        ('EXPENSE', 'Expense Claim Update'),
        ('HELPDESK', 'Helpdesk Ticket Response'),
        ('PERFORMANCE', 'Performance Review Notification'),
        ('LMS', 'Learning Course Update'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INFO')
    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} [{'Read' if self.is_read else 'Unread'}]"
