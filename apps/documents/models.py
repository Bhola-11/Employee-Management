from django.db import models
from apps.core.models import TimeStampedModel, StatusModel

class DocumentCategory(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='doc_categories')
    name = models.CharField(max_length=100) # Company Policies, Security Guidelines, NDA & Legal, Employment Handbooks
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class CompanyDocument(TimeStampedModel):
    ACCESS_CHOICES = (
        ('PUBLIC_ALL', 'All Organization Employees'),
        ('MANAGERS_ONLY', 'Department Managers & Executive'),
        ('HR_ONLY', 'HR & Legal Only'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='documents')
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=20, default='1.0')
    access_level = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='PUBLIC_ALL')
    file_attachment = models.FileField(upload_to='company_docs/')
    effective_date = models.DateField()
    description = models.TextField(blank=True)
    is_mandatory_acknowledgement = models.BooleanField(default=False)

    class Meta:
        ordering = ['-effective_date', 'title']

    def __str__(self):
        return f"{self.title} (v{self.version})"
