from django.test import TestCase
from decimal import Decimal
from apps.organizations.models import Organization, Department
from apps.recruitment.models import JobRequisition, RecruitmentStage, Candidate, JobApplication
from apps.recruitment.services import RecruitmentService

class RecruitmentATSTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='TechCorp ATS', code='TCA')
        self.dept = Department.objects.create(organization=self.org, name='Engineering', code='ENG')
        self.req = JobRequisition.objects.create(
            organization=self.org, title='Lead Backend Architect', code='REQ-101',
            department=self.dept, number_of_openings=2, status='OPEN', min_salary=Decimal('150000'), max_salary=Decimal('200000')
        )
        self.stage_apply = RecruitmentStage.objects.create(organization=self.org, name='Applied', order=1)
        self.stage_interview = RecruitmentStage.objects.create(organization=self.org, name='Technical Interview', order=2)
        self.stage_hired = RecruitmentStage.objects.create(organization=self.org, name='Hired', order=3, is_terminal=True)
        
        self.candidate = Candidate.objects.create(
            organization=self.org, first_name='Sarah', last_name='Connor',
            email='sarah.connor@example.com', phone='+1-555-4321', total_experience_years=Decimal('6.5')
        )
        self.app = JobApplication.objects.create(
            requisition=self.req, candidate=self.candidate, current_stage=self.stage_apply, status='IN_REVIEW'
        )

    def test_requisition_and_application_created(self):
        self.assertEqual(self.req.applications.count(), 1)
        self.assertEqual(self.app.candidate.full_name, 'Sarah Connor')

    def test_pipeline_summary_service(self):
        summary = RecruitmentService.get_pipeline_summary(self.org)
        self.assertEqual(summary['total_open_positions'], 1)
        self.assertEqual(summary['total_candidates'], 1)
        self.assertEqual(summary['active_applications'], 1)
