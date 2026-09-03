from django.test import TestCase
from apps.organizations.models import Organization
from apps.accounts.models import User
from apps.notifications.models import Notification
from apps.notifications.services import NotificationService

class NotificationEngineTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='AlertNet Corp', code='ANC')
        self.user = User.objects.create_user(
            email='tim@alertnet.com', username='tim@alertnet.com', password='Password@123', organization=self.org
        )

    def test_send_and_read_notification(self):
        notif = NotificationService.send_notification(
            user=self.user,
            title='Payslip Ready for Download',
            message='Your salary payslip for March 2026 has been generated.',
            notification_type='PAYROLL',
            action_url='/payroll/'
        )
        self.assertFalse(notif.is_read)
        self.assertEqual(self.user.notifications.filter(is_read=False).count(), 1)
        
        # Mark as read
        read_n = NotificationService.mark_as_read(notif.id, self.user)
        self.assertTrue(read_n.is_read)
        self.assertIsNotNone(read_n.read_at)
        self.assertEqual(self.user.notifications.filter(is_read=False).count(), 0)
