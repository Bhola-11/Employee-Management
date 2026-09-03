from django.test import TestCase
from apps.organizations.models import Organization, Department
from apps.analytics.models import ScheduledReport
from apps.analytics.services import AnalyticsService

class ExecutiveAnalyticsTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Insight Corp', code='ISC')
        self.dept = Department.objects.create(organization=self.org, name='Data Science', code='DS')

    def test_executive_summary_service(self):
        summary = AnalyticsService.get_executive_summary(self.org)
        self.assertIn('total_headcount', summary)
        self.assertIn('dept_breakdown', summary)
        self.assertIn('payroll_trends', summary)

    def test_scheduled_report_creation(self):
        rep = ScheduledReport.objects.create(
            organization=self.org, name='Monthly Board Digest', report_type='HEADCOUNT',
            frequency='MONTHLY', recipients_emails='board@insight.io'
        )
        self.assertEqual(rep.frequency, 'MONTHLY')
        self.assertTrue(rep.is_active)
