from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.travel.models import TravelRequisition

class TravelRequisitionTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='JetSet Global', code='JSG')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-TRV-01', first_name='Buzz', last_name='Aldrin',
            work_email='buzz@jetset.com', phone_number='+1-555-1111',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )

    def test_travel_requisition_flow(self):
        trav = TravelRequisition.objects.create(
            organization=self.org, employee=self.emp, requisition_number='TRV-7788',
            purpose='CLIENT_MEETING', description='Client onsite architectural review',
            origin_city='San Francisco', destination_city='Tokyo',
            departure_date=date(2026, 5, 1), return_date=date(2026, 5, 8),
            estimated_budget=Decimal('3500.00'), status='PENDING_MANAGER'
        )
        self.assertEqual(trav.destination_city, 'Tokyo')
        self.assertEqual(trav.status, 'PENDING_MANAGER')
