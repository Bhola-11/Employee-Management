from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class ExpenseCategory(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=100) # Travel & Lodging, Client Entertainment, Tech Equipment, Office Supplies, Certification
    code = models.CharField(max_length=50)
    requires_receipt = models.BooleanField(default=True)
    max_limit_per_claim = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('5000.00'))
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class ExpenseClaim(TimeStampedModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted / Awaiting Manager'),
        ('MANAGER_APPROVED', 'Approved by Manager - Awaiting Finance'),
        ('FINANCE_APPROVED', 'Approved by Finance - Queued for Payout'),
        ('PAID', 'Reimbursed & Paid'),
        ('REJECTED', 'Rejected'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='expense_claims')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='expense_claims')
    claim_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200) # e.g. Q1 Client Summit Chicago Travel Expenses
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    submitted_date = models.DateField(auto_now_add=True)
    
    reviewed_by_manager = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='manager_reviewed_claims')
    manager_action_date = models.DateTimeField(null=True, blank=True)
    finance_auditor = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='finance_reviewed_claims')
    payout_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_total(self):
        tot = sum(item.amount for item in self.items.all())
        self.total_amount = tot
        self.save(update_fields=['total_amount'])
        return tot

    def __str__(self):
        return f"Claim #{self.claim_number} - {self.employee.full_name} (${self.total_amount})"


class ExpenseItem(TimeStampedModel):
    claim = models.ForeignKey(ExpenseClaim, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='items')
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_name = models.CharField(max_length=150) # e.g. Delta Airlines, Hilton Hotel, AWS
    description = models.CharField(max_length=255)
    receipt_file = models.FileField(upload_to='receipts/', null=True, blank=True)

    class Meta:
        ordering = ['expense_date']

    def __str__(self):
        return f"{self.merchant_name}: ${self.amount} ({self.category.name})"
