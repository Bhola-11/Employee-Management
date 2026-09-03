from django.test import TestCase
from datetime import date
from apps.organizations.models import Organization
from apps.employees.models import Employee
from apps.learning.models import Course, CourseModule, CourseEnrollment

class LMSTrainingTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='LearnTech Academy', code='LTA')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-LRN-01', first_name='Ken', last_name='Thompson',
            work_email='ken@learntech.com', phone_number='+1-555-3434',
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.course = Course.objects.create(
            organization=self.org, title='Distributed Systems Architecture', code='DSA-401',
            category='Engineering', duration_hours=6.0, description='Advanced distributed consensus.'
        )
        self.module = CourseModule.objects.create(
            course=self.course, title='Raft Consensus Protocol', order=1, duration_minutes=45
        )

    def test_course_enrollment(self):
        enr = CourseEnrollment.objects.create(
            employee=self.emp, course=self.course, status='IN_PROGRESS', progress_percentage=50
        )
        self.assertEqual(enr.course.code, 'DSA-401')
        self.assertEqual(enr.progress_percentage, 50)
