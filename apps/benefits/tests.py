from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.benefits.models import BenefitPlan, EmployeeBenefitEnrollment

class BenefitsAdministrationTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='BenefitCare Org', code='BCO')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-BEN-01', first_name='Linus', last_name='Torvalds',
            work_email='linus@benefitcare.com', phone_number='+1-555-7777',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.plan = BenefitPlan.objects.create(
            organization=self.org, name='Premier Health Platinum', code='PLT-HLTH',
            category='HEALTH_INSURANCE', provider_name='Blue Cross Shield',
            employer_monthly_contribution=Decimal('600.00'), employee_monthly_contribution=Decimal('150.00')
        )

    def test_benefit_enrollment(self):
        enr = EmployeeBenefitEnrollment.objects.create(
            employee=self.emp, plan=self.plan, enrolled_date=date(2026, 1, 1),
            nominee_name='Tove Torvalds', nominee_relationship='Spouse', status='ACTIVE'
        )
        self.assertEqual(enr.plan.provider_name, 'Blue Cross Shield')
        self.assertEqual(self.emp.benefit_enrollments.count(), 1)
