from django.utils import timezone
from .models import Notification

class NotificationService:
    @staticmethod
    def send_notification(user, title, message, notification_type='INFO', action_url=''):
        notif = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
            is_read=False
        )
        return notif

    @staticmethod
    def mark_as_read(notification_id, user):
        try:
            notif = Notification.objects.get(id=notification_id, user=user)
            notif.is_read = True
            notif.read_at = timezone.now()
            notif.save(update_fields=['is_read', 'read_at'])
            return notif
        except Notification.DoesNotExist:
            return None
