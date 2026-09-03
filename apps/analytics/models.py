from django.db import models
from apps.core.models import TimeStampedModel

class ScheduledReport(TimeStampedModel):
    FREQUENCY_CHOICES = (
        ('DAILY', 'Daily Automated Snapshot'),
        ('WEEKLY', 'Weekly Summary Digest'),
        ('MONTHLY', 'Monthly Financial & Workforce Report'),
        ('QUARTERLY', 'Quarterly Executive Review'),
    )
    REPORT_TYPE_CHOICES = (
        ('HEADCOUNT', 'Headcount & Demographics Analysis'),
        ('PAYROLL', 'Payroll Expenditure & Statutory Deductions'),
        ('ATTENDANCE', 'Attendance, Overtime & Leave Utilization'),
        ('RECRUITMENT', 'Recruitment ATS Funnel & Velocity'),
        ('PERFORMANCE', 'Performance Ratings & OKR Progress'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='scheduled_reports')
    name = models.CharField(max_length=150)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='MONTHLY')
    recipients_emails = models.TextField(help_text='Comma-separated email addresses')
    is_active = models.BooleanField(default=True)
    last_generated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"
