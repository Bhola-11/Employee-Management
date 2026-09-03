import uuid
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class TenantModel(TimeStampedModel):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_items',
        db_index=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class StatusModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True
