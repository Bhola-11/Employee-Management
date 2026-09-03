import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, StatusModel

class Employee(TimeStampedModel, StatusModel):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('NON_BINARY', 'Non-Binary'),
        ('OTHER', 'Other / Prefer not to say'),
    )
    MARITAL_STATUS_CHOICES = (
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    )
    STATUS_CHOICES = (
        ('CANDIDATE', 'Candidate'),
        ('SELECTED', 'Selected'),
        ('OFFER_SENT', 'Offer Sent'),
        ('ONBOARDING', 'Onboarding'),
        ('PROBATION', 'Probation'),
        ('ACTIVE', 'Active Employee'),
        ('CONFIRMED', 'Confirmed'),
        ('NOTICE_PERIOD', 'Notice Period'),
        ('EXITED', 'Exited'),
        ('TERMINATED', 'Terminated'),
        ('RETIRED', 'Retired'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='employees')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    
    employee_id = models.CharField(max_length=50, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='MALE')
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='SINGLE')
    blood_group = models.CharField(max_length=10, blank=True)
    
    personal_email = models.EmailField(blank=True)
    work_email = models.EmailField(db_index=True)
    phone_number = models.CharField(max_length=30)
    alternate_phone = models.CharField(max_length=30, blank=True)
    profile_photo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Organizational Alignment
    branch = models.ForeignKey('organizations.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    designation = models.ForeignKey('organizations.Designation', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    job_level = models.ForeignKey('organizations.JobLevel', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    employment_type = models.ForeignKey('organizations.EmploymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    work_location = models.ForeignKey('organizations.WorkLocation', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    team = models.ForeignKey('organizations.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    direct_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    # Lifecycle & Dates
    joining_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    probation_end_date = models.DateField(null=True, blank=True)
    notice_period_days = models.PositiveIntegerField(default=30)
    employment_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)
    is_manager = models.BooleanField(default=False)
    biography = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'employee_id')
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['organization', 'employment_status']),
            models.Index(fields=['organization', 'department']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.employee_id})'

    @property
    def full_name(self):
        mid = f' {self.middle_name}' if self.middle_name else ''
        return f'{self.first_name}{mid} {self.last_name}'.strip()


class EmergencyContact(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100) # e.g. Spouse, Parent, Sibling
    phone_number = models.CharField(max_length=30)
    alternate_phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f'{self.name} ({self.relationship}) - {self.employee.full_name}'


class EmployeeAddress(TimeStampedModel):
    ADDRESS_TYPES = (
        ('PERMANENT', 'Permanent Address'),
        ('CURRENT', 'Current / Residential Address'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='CURRENT')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='United States')
    postal_code = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['address_type']

    def __str__(self):
        return f'{self.get_address_type_display()} - {self.city}, {self.country}'


class EmployeeEducation(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    degree_diploma = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    institution_name = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    grade_percentage = models.CharField(max_length=50, blank=True)
    activities = models.TextField(blank=True)

    class Meta:
        ordering = ['-end_year', '-start_year']

    def __str__(self):
        return f'{self.degree_diploma} in {self.field_of_study} ({self.institution_name})'


class EmployeePastExperience(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='past_experiences')
    company_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    job_description = models.TextField(blank=True)
    leaving_reason = models.CharField(max_length=255, blank=True)
    reference_contact = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.designation} at {self.company_name}'


class SkillCategory(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='skill_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class EmployeeSkill(TimeStampedModel):
    PROFICIENCY_LEVELS = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert / Lead'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='employee_skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='INTERMEDIATE')
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    is_certified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'skill')
        ordering = ['skill__name']

    def __str__(self):
        return f'{self.employee.full_name} - {self.skill.name} ({self.proficiency_level})'


class EmployeeBankDetail(TimeStampedModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_detail')
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=255)
    ifsc_swift_code = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255, blank=True)
    account_type = models.CharField(max_length=50, default='Checking')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bank_name} - {self.account_number[-4:]}'


class EmployeeTaxInfo(TimeStampedModel):
    REGIME_CHOICES = (
        ('NEW', 'New Simplified Tax Regime'),
        ('OLD', 'Old Tax Regime with Deductions'),
    )
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='tax_info')
    pan_ssn_number = models.CharField(max_length=50)
    tax_regime = models.CharField(max_length=20, choices=REGIME_CHOICES, default='NEW')
    pf_uan_number = models.CharField(max_length=50, blank=True)
    esic_number = models.CharField(max_length=50, blank=True)
    is_tax_exempt = models.BooleanField(default=False)

    def __str__(self):
        return f'Tax Info for {self.employee.full_name}'


class EmployeeStatutoryDocument(TimeStampedModel):
    DOC_TYPES = (
        ('PASSPORT', 'Passport'),
        ('NATIONAL_ID', 'National ID / SSN Card'),
        ('DRIVING_LICENSE', 'Driver License'),
        ('TAX_CARD', 'Tax / PAN Card'),
        ('EDUCATION_CERT', 'Degree / Educational Certificate'),
        ('EXPERIENCE_LETTER', 'Relieving / Experience Letter'),
        ('OTHER', 'Other Identification'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified & Approved'),
        ('REJECTED', 'Rejected'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='statutory_documents')
    document_type = models.CharField(max_length=30, choices=DOC_TYPES)
    document_number = models.CharField(max_length=100)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    document_file = models.FileField(upload_to='documents/', null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    verification_remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_document_type_display()} - {self.employee.full_name}'


class EmployeeLifecycleTransition(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='lifecycle_transitions')
    from_status = models.CharField(max_length=30, choices=Employee.STATUS_CHOICES)
    to_status = models.CharField(max_length=30, choices=Employee.STATUS_CHOICES)
    transition_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=255)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-transition_date']

    def __str__(self):
        return f'{self.employee.full_name}: {self.from_status} -> {self.to_status}'
