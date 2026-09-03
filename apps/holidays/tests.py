from django.test import TestCase
from datetime import date
from apps.organizations.models import Organization, Branch
from apps.holidays.models import Holiday

class HolidayCalendarTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Global Holidays Ltd', code='GHL')
        self.branch_ny = Branch.objects.create(organization=self.org, name='New York', code='NY-01')

    def test_create_global_and_branch_holiday(self):
        h_global = Holiday.objects.create(
            organization=self.org, name="New Year's Day", date=date(2026, 1, 1), is_optional=False
        )
        h_ny = Holiday.objects.create(
            organization=self.org, branch=self.branch_ny, name="Empire State Day", date=date(2026, 7, 10)
        )
        self.assertEqual(self.org.holidays.count(), 2)
        self.assertEqual(self.branch_ny.holidays.count(), 1)
