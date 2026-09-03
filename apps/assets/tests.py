from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.assets.models import AssetCategory, Asset

class AssetGovernanceTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='AssetGov Corp', code='AGC')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-AST-01', first_name='Dennis', last_name='Ritchie',
            work_email='dennis@assetgov.com', phone_number='+1-555-5656',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.cat = AssetCategory.objects.create(organization=self.org, name='Laptops', code='LAPTOP')

    def test_asset_creation_and_assignment(self):
        asset = Asset.objects.create(
            organization=self.org, category=self.cat, asset_tag='AST-MBP-101',
            name='MacBook Pro 16 M3 Max', serial_number='C02G8901ABCD',
            status='ALLOCATED', assigned_to=self.emp, purchase_cost=Decimal('3499.00')
        )
        self.assertEqual(asset.assigned_to.full_name, 'Dennis Ritchie')
        self.assertEqual(asset.status, 'ALLOCATED')
