from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.core.models import TimeStampedModel, StatusModel

class JobRequisition(TimeStampedModel, StatusModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open & Active'),
        ('ON_HOLD', 'On Hold'),
        ('FILLED', 'Position Filled'),
        ('CANCELLED', 'Cancelled'),
    )
    EXPERIENCE_LEVEL_CHOICES = (
        ('ENTRY', 'Entry Level (0-2 yrs)'),
        ('MID', 'Mid Level (2-5 yrs)'),
        ('SENIOR', 'Senior Level (5-8 yrs)'),
        ('LEAD', 'Lead / Principal (8+ yrs)'),
        ('EXECUTIVE', 'Executive (12+ yrs)'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='job_requisitions')
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_requisitions')
    branch = models.ForeignKey('organizations.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_requisitions')
    job_level = models.ForeignKey('organizations.JobLevel', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_requisitions')
    employment_type = models.ForeignKey('organizations.EmploymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_requisitions')
    
    number_of_openings = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='MID')
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    target_hire_date = models.DateField(null=True, blank=True)
    
    hiring_manager = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='hiring_requisitions')
    lead_recruiter = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='recruiter_requisitions')
    
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.code}) - {self.organization.code}"


class RecruitmentStage(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='recruitment_stages')
    name = models.CharField(max_length=100) # Sourced, Screened, Technical Round, Cultural Fit, Offer, Hired, Rejected
    order = models.PositiveSmallIntegerField(default=1)
    is_terminal = models.BooleanField(default=False) # Hired or Rejected

    class Meta:
        ordering = ['order']
        unique_together = ('organization', 'name')

    def __str__(self):
        return f"{self.order}. {self.name}"


class Candidate(TimeStampedModel):
    SOURCE_CHOICES = (
        ('PORTAL', 'Company Career Portal'),
        ('LINKEDIN', 'LinkedIn Sourced'),
        ('REFERRAL', 'Internal Employee Referral'),
        ('AGENCY', 'Recruitment Agency'),
        ('CAMPUS', 'Campus Drive'),
        ('OTHER', 'Other Channel'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='candidates')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=30)
    current_company = models.CharField(max_length=255, blank=True)
    current_designation = models.CharField(max_length=255, blank=True)
    total_experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal('0.0'))
    current_ctc = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    expected_ctc = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notice_period_days = models.PositiveIntegerField(default=30)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='PORTAL')
    referred_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_candidates')
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class JobApplication(TimeStampedModel):
    STATUS_CHOICES = (
        ('IN_REVIEW', 'In Review'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEWING', 'Interviewing'),
        ('OFFERED', 'Offer Extended'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn by Candidate'),
    )
    requisition = models.ForeignKey(JobRequisition, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    current_stage = models.ForeignKey(RecruitmentStage, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_REVIEW')
    overall_rating = models.PositiveSmallIntegerField(default=0) # 1-5
    applied_date = models.DateField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        unique_together = ('requisition', 'candidate')
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.candidate.full_name} -> {self.requisition.title}"


class InterviewSchedule(TimeStampedModel):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    )
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    title = models.CharField(max_length=255) # e.g. Technical Round 1 - System Architecture
    interviewers = models.ManyToManyField('employees.Employee', related_name='scheduled_interviews')
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    meeting_link = models.URLField(blank=True)
    location_room = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ['-scheduled_start']

    def __str__(self):
        return f"{self.title} for {self.application.candidate.full_name}"


class InterviewFeedback(TimeStampedModel):
    RECOMMENDATION_CHOICES = (
        ('STRONG_HIRE', 'Strong Hire'),
        ('HIRE', 'Hire'),
        ('NEUTRAL', 'Neutral / Borderline'),
        ('DO_NOT_HIRE', 'Do Not Hire'),
    )
    interview = models.ForeignKey(InterviewSchedule, on_delete=models.CASCADE, related_name='feedback_entries')
    interviewer = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='given_feedbacks')
    technical_score = models.PositiveSmallIntegerField(default=3) # 1-5
    communication_score = models.PositiveSmallIntegerField(default=3) # 1-5
    culture_fit_score = models.PositiveSmallIntegerField(default=3) # 1-5
    overall_score = models.PositiveSmallIntegerField(default=3) # 1-5
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES, default='HIRE')
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    summary_comments = models.TextField()

    def __str__(self):
        return f"Feedback by {self.interviewer.full_name} ({self.recommendation})"


class JobOffer(TimeStampedModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PENDING_APPROVAL', 'Pending Executive Approval'),
        ('SENT', 'Offer Sent to Candidate'),
        ('ACCEPTED', 'Accepted by Candidate'),
        ('DECLINED', 'Declined by Candidate'),
        ('EXPIRED', 'Expired'),
        ('WITHDRAWN', 'Withdrawn'),
    )
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='job_offer')
    offered_salary = models.DecimalField(max_digits=12, decimal_places=2)
    variable_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sign_on_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    joining_date = models.DateField()
    offer_expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    special_terms = models.TextField(blank=True)
    offer_letter_document = models.FileField(upload_to='offer_letters/', null=True, blank=True)

    def __str__(self):
        return f"Offer for {self.application.candidate.full_name} ({self.status})"
