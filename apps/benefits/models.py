from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class BenefitPlan(TimeStampedModel, StatusModel):
    CATEGORY_CHOICES = (
        ('HEALTH_INSURANCE', 'Comprehensive Health Insurance'),
        ('DENTAL_VISION', 'Dental & Vision Care'),
        ('RETIREMENT_401K', '401(k) / Provident Fund Match'),
        ('LIFE_DISABILITY', 'Life & Disability Insurance'),
        ('WELLNESS_STIPEND', 'Wellness & Gym Stipend'),
        ('MEAL_VOUCHER', 'Meal & Nutrition Allowance'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='benefit_plans')
    name = models.CharField(max_length=150) # e.g. Premier Gold PPO Health Plan
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    provider_name = models.CharField(max_length=150) # e.g. Blue Cross Blue Shield, Fidelity
    
    employer_monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    employee_monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True)
    terms_document = models.FileField(upload_to='benefits/', null=True, blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.provider_name})"


class EmployeeBenefitEnrollment(TimeStampedModel):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active & Covered'),
        ('PENDING_APPROVAL', 'Pending Enrollment Review'),
        ('OPTED_OUT', 'Opted Out by Employee'),
        ('TERMINATED', 'Coverage Terminated'),
    )
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='benefit_enrollments')
    plan = models.ForeignKey(BenefitPlan, on_delete=models.CASCADE, related_name='enrolled_employees')
    enrolled_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    nominee_name = models.CharField(max_length=150, blank=True)
    nominee_relationship = models.CharField(max_length=50, blank=True)
    custom_employee_deduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'plan')
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.employee.full_name} -> {self.plan.name} [{self.status}]"
