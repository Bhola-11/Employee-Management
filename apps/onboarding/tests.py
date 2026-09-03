from django.test import TestCase
from datetime import date
from apps.organizations.models import Organization, Branch, Department
from apps.employees.models import Employee
from apps.onboarding.models import OnboardingTemplate, OnboardingTaskTemplate, EmployeeOnboarding, OnboardingTask
from apps.onboarding.services import OnboardingService

class OnboardingWorkflowTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Global Onboarding Inc', code='GOI')
        self.dept = Department.objects.create(organization=self.org, name='Operations', code='OPS')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-OB-01', first_name='John', last_name='Doe',
            work_email='john.doe@goi.com', phone_number='+1-555-9988', department=self.dept,
            joining_date=date(2026, 2, 1), employment_status='ACTIVE'
        )
        self.tpl = OnboardingTemplate.objects.create(organization=self.org, name='Standard Developer Onboarding', department=self.dept)
        OnboardingTaskTemplate.objects.create(template=self.tpl, title='Setup Workstation', category='IT', due_day_offset=1)
        OnboardingTaskTemplate.objects.create(template=self.tpl, title='Sign NDA', category='HR', due_day_offset=1)

    def test_instantiate_onboarding_and_progress(self):
        ob = EmployeeOnboarding.objects.create(
            employee=self.emp, template=self.tpl, start_date=date(2026, 2, 1),
            target_completion_date=date(2026, 2, 15), status='IN_PROGRESS'
        )
        OnboardingService.instantiate_onboarding(ob, user=None)
        self.assertEqual(ob.tasks.count(), 2)
        self.assertEqual(ob.completion_percentage, 0)
        
        # Complete one task
        task = ob.tasks.first()
        task.status = 'COMPLETED'
        task.save()
        prog = ob.calculate_progress()
        self.assertEqual(prog, 50)
