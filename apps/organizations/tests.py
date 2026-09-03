from django.test import TestCase
from decimal import Decimal
from apps.organizations.models import Organization, Branch, Department, JobLevel, Designation, EmploymentType

class OrganizationStructureTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Globex Tech', code='GLX', currency='USD')
        self.branch = Branch.objects.create(organization=self.org, name='HQ', code='HQ-01', is_headquarters=True)
        self.dept = Department.objects.create(organization=self.org, name='Engineering', code='ENG', budget=Decimal('1000000'))
        self.level = JobLevel.objects.create(organization=self.org, level_name='Senior Specialist', rank_order=3)
        self.desig = Designation.objects.create(organization=self.org, title='Senior Backend Dev', code='SR-BE', department=self.dept, job_level=self.level)
        self.emp_type = EmploymentType.objects.create(organization=self.org, name='Full-Time', code='FT')

    def test_organization_created(self):
        self.assertEqual(self.org.code, 'GLX')
        self.assertTrue(self.branch.is_headquarters)

    def test_department_relationship(self):
        self.assertEqual(self.dept.organization, self.org)
        self.assertEqual(self.desig.department, self.dept)
        self.assertEqual(self.desig.job_level.rank_order, 3)
