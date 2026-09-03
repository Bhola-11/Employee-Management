from django.test import TestCase
from datetime import date
from apps.organizations.models import Organization
from apps.documents.models import DocumentCategory, CompanyDocument

class DocumentRepositoryTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='DocVault Corp', code='DVC')
        self.cat = DocumentCategory.objects.create(organization=self.org, name='Compliance Policies', code='COMPLIANCE')

    def test_document_publishing(self):
        doc = CompanyDocument.objects.create(
            organization=self.org, category=self.cat, title='Global Code of Conduct 2026',
            version='2.1', access_level='PUBLIC_ALL', effective_date=date(2026, 1, 1)
        )
        self.assertEqual(doc.version, '2.1')
        self.assertEqual(doc.access_level, 'PUBLIC_ALL')
