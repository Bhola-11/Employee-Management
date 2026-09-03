from django.test import TestCase
from decimal import Decimal
from apps.organizations.models import Organization, JobLevel
from apps.compensation.models import SalaryBand, SalaryComponent

class CompensationTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='CompTech Corp', code='CTC')
        self.level = JobLevel.objects.create(organization=self.org, level_name='Staff Engineer', rank_order=4)

    def test_salary_band_and_components(self):
        band = SalaryBand.objects.create(
            organization=self.org, job_level=self.level, name='Staff Engineering Band', code='BAND-L4',
            min_base_salary=Decimal('140000'), mid_base_salary=Decimal('175000'), max_base_salary=Decimal('210000')
        )
        comp = SalaryComponent.objects.create(
            organization=self.org, name='Basic Pay', code='BASIC', component_type='EARNING', calculation_type='FIXED'
        )
        self.assertEqual(band.mid_base_salary, Decimal('175000'))
        self.assertEqual(comp.component_type, 'EARNING')
