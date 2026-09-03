from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization, Branch, Department, JobLevel, Designation, EmploymentType
from apps.employees.models import Employee, EmployeeLifecycleTransition

class EmployeeLifecycleTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Initech Global', code='INT')
        self.branch = Branch.objects.create(organization=self.org, name='Austin Office', code='ATX')
        self.dept = Department.objects.create(organization=self.org, name='DevOps', code='OPS')
        self.level = JobLevel.objects.create(organization=self.org, level_name='Lead', rank_order=4)
        self.desig = Designation.objects.create(organization=self.org, title='SRE Lead', code='SRE-LD', department=self.dept, job_level=self.level)
        self.emp_type = EmploymentType.objects.create(organization=self.org, name='Permanent Full-Time', code='FT-P')
        
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-1001', first_name='Peter', last_name='Gibbons',
            work_email='peter@initech.com', phone_number='+1-555-0101', designation=self.desig,
            department=self.dept, job_level=self.level, branch=self.branch, employment_type=self.emp_type,
            joining_date=date(2023, 1, 1), employment_status='PROBATION'
        )

    def test_employee_initial_state(self):
        self.assertEqual(self.emp.full_name, 'Peter Gibbons')
        self.assertEqual(self.emp.employment_status, 'PROBATION')

    def test_lifecycle_transition(self):
        EmployeeLifecycleTransition.objects.create(
            employee=self.emp, from_status='PROBATION', to_status='CONFIRMED',
            reason='Passed 90-day review with honors.'
        )
        self.emp.employment_status = 'CONFIRMED'
        self.emp.save()
        self.assertEqual(self.emp.lifecycle_transitions.count(), 1)
        self.assertEqual(self.emp.lifecycle_transitions.first().to_status, 'CONFIRMED')
