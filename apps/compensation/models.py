from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class SalaryBand(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='salary_bands')
    job_level = models.ForeignKey('organizations.JobLevel', on_delete=models.CASCADE, related_name='salary_bands')
    name = models.CharField(max_length=100) # e.g. Band L3 Senior Specialist Band
    code = models.CharField(max_length=50)
    min_base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    mid_base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    max_base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    target_annual_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['job_level__rank_order', 'name']

    def __str__(self):
        return f"{self.name} (${self.min_base_salary} - ${self.max_base_salary})"


class SalaryComponent(TimeStampedModel, StatusModel):
    TYPE_CHOICES = (
        ('EARNING', 'Earning / Allowance'),
        ('DEDUCTION', 'Deduction / Withholding'),
    )
    CALC_TYPE_CHOICES = (
        ('FIXED', 'Fixed Flat Amount'),
        ('PERCENTAGE_BASIC', 'Percentage of Basic Pay'),
        ('FORMULA', 'Custom Formula Calculation'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='salary_components')
    name = models.CharField(max_length=100) # Basic Pay, HRA, Special Allowance, Medical, Provident Fund, Tax
    code = models.CharField(max_length=50)
    component_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='EARNING')
    calculation_type = models.CharField(max_length=30, choices=CALC_TYPE_CHOICES, default='FIXED')
    percentage_value = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    is_taxable = models.BooleanField(default=True)
    is_statutory = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['component_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_component_type_display()})"
