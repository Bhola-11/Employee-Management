from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class AppraisalCycle(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='appraisal_cycles')
    name = models.CharField(max_length=150) # e.g. Annual Performance Review 2026, Q1 Mid-Year Review
    start_date = models.DateField()
    end_date = models.DateField()
    self_review_deadline = models.DateField()
    manager_review_deadline = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date.year})"


class GoalObjective(TimeStampedModel, StatusModel):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical / Strategic'),
    )
    STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed / Achieved'),
        ('BEHIND', 'Behind Schedule'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='performance_goals')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='performance_goals')
    title = models.CharField(max_length=255) # e.g. Achieve 99.99% Cloud Service Uptime, Hire 15 Senior Engineers
    category = models.CharField(max_length=100, default='Operational Excellence')
    target_date = models.DateField()
    progress_percentage = models.PositiveSmallIntegerField(default=0)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    key_metric = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-target_date']

    def __str__(self):
        return f"{self.title} - {self.employee.full_name} ({self.progress_percentage}%)"


class EmployeeAppraisal(TimeStampedModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft / Self-Review Pending'),
        ('SUBMITTED_SELF', 'Self-Review Submitted - Awaiting Manager'),
        ('MANAGER_EVALUATED', 'Manager Review Completed'),
        ('CALIBRATED', 'Final Calibrated & Closed'),
    )
    RATING_CHOICES = (
        (1, '1 - Needs Immediate Improvement'),
        (2, '2 - Partially Meets Expectations'),
        (3, '3 - Fully Meets Expectations (Strong Contributor)'),
        (4, '4 - Exceeds Expectations (High Impact)'),
        (5, '5 - Exceptional / Role Model (Top 5%)'),
    )
    cycle = models.ForeignKey(AppraisalCycle, on_delete=models.CASCADE, related_name='appraisals')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='appraisals')
    manager = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_appraisals')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    
    self_achievements = models.TextField(blank=True)
    self_areas_for_growth = models.TextField(blank=True)
    self_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    
    manager_feedback = models.TextField(blank=True)
    manager_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    final_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True) # e.g. 4.2
    
    promotion_recommended = models.BooleanField(default=False)
    recommended_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('cycle', 'employee')
        ordering = ['-cycle__start_date', 'employee__first_name']

    def __str__(self):
        return f"Appraisal: {self.employee.full_name} ({self.cycle.name})"
