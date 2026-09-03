import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class ActivityLog(TimeStampedModel):
    ACTION_CHOICES = (
        ('CREATE', 'Create Record'),
        ('UPDATE', 'Update Record'),
        ('DELETE', 'Delete Record'),
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('VIEW', 'View Sensitive Data'),
        ('EXPORT', 'Data Export'),
        ('STATUS_CHANGE', 'Status Transition'),
        ('APPROVE', 'Workflow Approval'),
        ('REJECT', 'Workflow Rejection'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_activities'
    )
    action_type = models.CharField(max_length=30, choices=ACTION_CHOICES, db_index=True)
    module_name = models.CharField(max_length=50, db_index=True)
    object_id = models.CharField(max_length=100, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    changes_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'module_name']),
            models.Index(fields=['organization', 'action_type']),
        ]

    def __str__(self):
        user_str = self.user.email if self.user else 'System'
        return f'[{self.action_type}] {self.module_name}: {self.object_repr} by {user_str}'


class ModelChangeLog(TimeStampedModel):
    activity = models.ForeignKey(ActivityLog, on_delete=models.CASCADE, related_name='field_changes')
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    class Meta:
        ordering = ['field_name']

    def __str__(self):
        return f'{self.field_name}: {self.old_value} -> {self.new_value}'
