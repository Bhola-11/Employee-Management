from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.expenses.models import ExpenseCategory, ExpenseClaim, ExpenseItem

class ExpenseClaimTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='SpendWise Corp', code='SWC')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-EXP-01', first_name='Margaret', last_name='Hamilton',
            work_email='margaret@spendwise.com', phone_number='+1-555-6543',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.cat_travel = ExpenseCategory.objects.create(
            organization=self.org, name='Travel & Airfare', code='TRV'
        )
        self.cat_meals = ExpenseCategory.objects.create(
            organization=self.org, name='Client Meals & Dining', code='MEALS'
        )

    def test_claim_total_calculation(self):
        claim = ExpenseClaim.objects.create(
            organization=self.org, employee=self.emp, claim_number='EXP-9901',
            title='NASA Conference Travel Reimbursement', status='SUBMITTED'
        )
        ExpenseItem.objects.create(
            claim=claim, category=self.cat_travel, expense_date=date(2026, 2, 10),
            amount=Decimal('450.00'), merchant_name='United Airlines', description='Flight to Houston'
        )
        ExpenseItem.objects.create(
            claim=claim, category=self.cat_meals, expense_date=date(2026, 2, 11),
            amount=Decimal('85.50'), merchant_name='The Palm Restaurant', description='Dinner with client'
        )
        tot = claim.calculate_total()
        self.assertEqual(tot, Decimal('535.50'))
        self.assertEqual(claim.total_amount, Decimal('535.50'))
