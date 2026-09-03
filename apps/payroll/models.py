from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class PayrollCycle(TimeStampedModel, StatusModel):
    CYCLE_TYPE_CHOICES = (
        ('MONTHLY', 'Monthly Calendar Cycle'),
        ('BI_WEEKLY', 'Bi-Weekly (Every 2 Weeks)'),
        ('SEMI_MONTHLY', 'Semi-Monthly (Twice a Month)'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='payroll_cycles')
    name = models.CharField(max_length=100) # e.g. Monthly Standard Cycle
    cycle_type = models.CharField(max_length=20, choices=CYCLE_TYPE_CHOICES, default='MONTHLY')
    start_day = models.PositiveSmallIntegerField(default=1) # 1st of month
    end_day = models.PositiveSmallIntegerField(default=30)
    payout_day = models.PositiveSmallIntegerField(default=1) # Next month payout

    def __str__(self):
        return f"{self.name} ({self.organization.code})"


class PayrollRun(TimeStampedModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft / Calculating'),
        ('UNDER_REVIEW', 'Under Finance Review'),
        ('APPROVED', 'Approved by Executive'),
        ('LOCKED', 'Finalized & Locked for Disbursal'),
        ('DISBURSED', 'Funds Disbursed to Bank'),
        ('CANCELLED', 'Cancelled'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='payroll_runs')
    payroll_cycle = models.ForeignKey(PayrollCycle, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150) # e.g. Payroll Run - March 2026
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField() # 1-12
    
    total_employees_count = models.PositiveIntegerField(default=0)
    total_gross_pay = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_net_pay = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_employer_contributions = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    run_date = models.DateField(auto_now_add=True)
    processed_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payroll_runs')
    approved_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payroll_runs')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.name} [{self.status}]"


class EmployeeSalaryStructure(TimeStampedModel):
    employee = models.OneToOneField('employees.Employee', on_delete=models.CASCADE, related_name='salary_structure')
    annual_ctc = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_gross = models.DecimalField(max_digits=12, decimal_places=2)
    basic_pay_monthly = models.DecimalField(max_digits=12, decimal_places=2)
    hra_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    special_allowance_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    provident_fund_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    professional_tax_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    effective_from = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Structure: {self.employee.full_name} (${self.annual_ctc}/yr)"


class Payslip(TimeStampedModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('GENERATED', 'Generated & Verified'),
        ('PUBLISHED', 'Published to Employee Self-Service'),
        ('PAID', 'Paid / Disbursed'),
    )
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='payslips')
    payslip_number = models.CharField(max_length=50, unique=True)
    
    working_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('22.0'))
    payable_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('22.0'))
    loss_of_pay_days = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_rent_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    special_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    bonus_incentives = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    gross_earnings = models.DecimalField(max_digits=12, decimal_places=2)
    
    income_tax_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    provident_fund_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    medical_insurance_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GENERATED')
    payment_method = models.CharField(max_length=50, default='DIRECT_DEPOSIT')
    bank_account_masked = models.CharField(max_length=50, blank=True)
    pdf_file = models.FileField(upload_to='payslips/', null=True, blank=True)

    class Meta:
        ordering = ['-payroll_run__year', '-payroll_run__month', 'employee__first_name']

    def __str__(self):
        return f"Payslip #{self.payslip_number} - {self.employee.full_name} (${self.net_salary})"
