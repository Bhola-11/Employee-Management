from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.performance.models import AppraisalCycle, GoalObjective, EmployeeAppraisal

class PerformanceAppraisalTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='PerfCorp Global', code='PCG')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-PRF-01', first_name='Guido', last_name='van Rossum',
            work_email='guido@perfcorp.com', phone_number='+1-555-1212',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.cycle = AppraisalCycle.objects.create(
            organization=self.org, name='Annual Review 2026',
            start_date=date(2026, 1, 1), end_date=date(2026, 12, 31),
            self_review_deadline=date(2026, 11, 15), manager_review_deadline=date(2026, 12, 1)
        )

    def test_goal_and_appraisal_lifecycle(self):
        goal = GoalObjective.objects.create(
            organization=self.org, employee=self.emp, title='Design Python 4 AST Spec',
            target_date=date(2026, 6, 30), progress_percentage=75, status='IN_PROGRESS'
        )
        appraisal = EmployeeAppraisal.objects.create(
            cycle=self.cycle, employee=self.emp, status='DRAFT', self_rating=5
        )
        self.assertEqual(goal.progress_percentage, 75)
        self.assertEqual(appraisal.self_rating, 5)
