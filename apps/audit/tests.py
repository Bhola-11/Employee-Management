from django.test import TestCase
from apps.organizations.models import Organization
from apps.audit.models import ActivityLog

class AuditComplianceTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Cyberdyne Corp', code='CYB')

    def test_activity_log_creation(self):
        log = ActivityLog.objects.create(
            organization=self.org, module_name='employees', action_type='CREATE',
            object_id='EMP-999', object_repr='John Connor', description='New employee onboarded.'
        )
        self.assertEqual(log.module_name, 'employees')
        self.assertEqual(log.action_type, 'CREATE')
        self.assertIn('John Connor', str(log))
