from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization, Department
from apps.employees.models import Employee
from apps.leave_management.models import LeaveType, LeaveBalance, LeaveApplication
from apps.leave_management.services import LeaveService

class LeaveManagementTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='LeaveTrack Corp', code='LTC')
        self.dept = Department.objects.create(organization=self.org, name='Finance', code='FIN')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-LV-01', first_name='Ada', last_name='Lovelace',
            work_email='ada.lovelace@ltc.com', phone_number='+1-555-8888', department=self.dept,
            joining_date=date(2024, 1, 1), employment_status='ACTIVE'
        )
        self.leave_type = LeaveType.objects.create(
            organization=self.org, name='Annual Paid Leave', code='PTO', annual_quota=Decimal('20.0')
        )
        self.balance = LeaveBalance.objects.create(
            organization=self.org, employee=self.emp, leave_type=self.leave_type, year=2026, allocated_days=Decimal('20.0')
        )

    def test_leave_application_and_balance_deduction(self):
        app = LeaveService.submit_application(
            employee=self.emp, leave_type=self.leave_type,
            start_date=date(2026, 4, 10), end_date=date(2026, 4, 12),
            reason='Family vacation trip'
        )
        self.assertEqual(app.number_of_days, Decimal('3.0'))
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.pending_days, Decimal('3.0'))
        self.assertEqual(self.balance.total_available, Decimal('17.0'))
        
        # Approve leave
        LeaveService.approve_application(app, reviewer=self.emp)
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.pending_days, Decimal('0.0'))
        self.assertEqual(self.balance.used_days, Decimal('3.0'))
        self.assertEqual(self.balance.total_available, Decimal('17.0'))
