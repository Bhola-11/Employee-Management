from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization, Department
from apps.employees.models import Employee
from apps.attendance.models import AttendanceRecord
from apps.attendance.services import AttendanceService

class AttendanceEngineTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='TimeTrack Corp', code='TTC')
        self.dept = Department.objects.create(organization=self.org, name='Tech', code='TECH')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-ATT-01', first_name='Alan', last_name='Turing',
            work_email='alan.turing@ttc.com', phone_number='+1-555-1234', department=self.dept,
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )

    def test_punch_in_and_punch_out(self):
        rec_in = AttendanceService.punch_in(self.emp, ip_address='192.168.1.100')
        self.assertIsNotNone(rec_in.clock_in)
        self.assertEqual(rec_in.status, 'PRESENT')
        
        rec_out = AttendanceService.punch_out(self.emp, ip_address='192.168.1.100')
        self.assertIsNotNone(rec_out.clock_out)
        self.assertEqual(rec_out.clock_out_ip, '192.168.1.100')
