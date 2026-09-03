from django.db import models
from apps.core.models import TimeStampedModel

class Holiday(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='holidays')
    branch = models.ForeignKey('organizations.Branch', on_delete=models.CASCADE, null=True, blank=True, related_name='holidays')
    name = models.CharField(max_length=255) # New Year's Day, Memorial Day, Christmas, Lunar New Year
    date = models.DateField(db_index=True)
    is_optional = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'branch', 'date')
        ordering = ['date']

    def __str__(self):
        loc = f" ({self.branch.city})" if self.branch else " (Global)"
        return f"{self.name} - {self.date}{loc}"
