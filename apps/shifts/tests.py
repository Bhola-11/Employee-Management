from django.test import TestCase
from datetime import date, time
from decimal import Decimal
from apps.organizations.models import Organization, Department
from apps.employees.models import Employee
from apps.shifts.models import ShiftType, ShiftRoster

class ShiftRosterTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='24-7 Support Hub', code='SSH')
        self.dept = Department.objects.create(organization=self.org, name='Support', code='SUP')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-SH-01', first_name='Grace', last_name='Hopper',
            work_email='grace.hopper@ssh.com', phone_number='+1-555-5555', department=self.dept,
            joining_date=date(2025, 5, 1), employment_status='ACTIVE'
        )
        self.shift_morning = ShiftType.objects.create(
            organization=self.org, name='Morning Standard', code='MORN',
            start_time=time(8, 0), end_time=time(17, 0), grace_period_minutes=15
        )

    def test_shift_roster_assignment(self):
        roster = ShiftRoster.objects.create(
            organization=self.org, employee=self.emp, shift_type=self.shift_morning,
            date=date(2026, 3, 1), is_weekly_off=False
        )
        self.assertEqual(roster.shift_type.code, 'MORN')
        self.assertFalse(roster.is_weekly_off)
