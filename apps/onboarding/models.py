from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, StatusModel

class OnboardingTemplate(TimeStampedModel, StatusModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='onboarding_templates')
    name = models.CharField(max_length=255)
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='onboarding_templates')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.organization.code})"


class OnboardingTaskTemplate(TimeStampedModel):
    CATEGORY_CHOICES = (
        ('HR', 'HR Documentation & Verification'),
        ('IT', 'IT Infrastructure & Access Provisioning'),
        ('FACILITIES', 'Facilities, Desk & Badge'),
        ('TRAINING', 'Orientation & Policy Training'),
        ('MANAGER', 'Manager Introduction & Goal Setting'),
    )
    template = models.ForeignKey(OnboardingTemplate, on_delete=models.CASCADE, related_name='task_templates')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='HR')
    description = models.TextField(blank=True)
    due_day_offset = models.IntegerField(default=1) # Days relative to joining date (e.g. -1 for pre-onboarding, 1 for Day 1)
    assignee_role = models.ForeignKey('accounts.Role', on_delete=models.SET_NULL, null=True, blank=True)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        ordering = ['due_day_offset', 'title']

    def __str__(self):
        return f"{self.title} (Day {self.due_day_offset})"


class EmployeeOnboarding(TimeStampedModel):
    STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
    )
    employee = models.OneToOneField('employees.Employee', on_delete=models.CASCADE, related_name='onboarding_workflow')
    template = models.ForeignKey(OnboardingTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    target_completion_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    completion_percentage = models.PositiveSmallIntegerField(default=0)
    buddy = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_buddies')
    notes = models.TextField(blank=True)

    def calculate_progress(self):
        total = self.tasks.count()
        if total == 0:
            return 100
        completed = self.tasks.filter(status='COMPLETED').count()
        progress = int((completed / total) * 100)
        self.completion_percentage = progress
        if progress == 100:
            self.status = 'COMPLETED'
        self.save(update_fields=['completion_percentage', 'status'])
        return progress

    def __str__(self):
        return f"Onboarding: {self.employee.full_name} ({self.completion_percentage}%)"


class OnboardingTask(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('BLOCKED', 'Blocked'),
    )
    onboarding = models.ForeignKey(EmployeeOnboarding, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default='HR')
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_onboarding_tasks')
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['due_date', 'status']

    def __str__(self):
        return f"{self.title} - {self.onboarding.employee.full_name} [{self.status}]"


class EmployeeOffboarding(TimeStampedModel):
    REASON_CHOICES = (
        ('RESIGNATION', 'Voluntary Resignation'),
        ('CAREER_GROWTH', 'Better Opportunity'),
        ('PERSONAL', 'Personal / Health Reasons'),
        ('TERMINATION', 'Company Termination'),
        ('RETIREMENT', 'Retirement'),
        ('CONTRACT_END', 'End of Fixed-Term Contract'),
    )
    STATUS_CHOICES = (
        ('INITIATED', 'Initiated / Notice Serving'),
        ('CLEARANCE_PENDING', 'Clearances In Progress'),
        ('READY_FOR_EXIT', 'Clearances Complete - Ready for Final Settlement'),
        ('COMPLETED', 'Offboarding Complete & Exited'),
        ('CANCELLED', 'Resignation Withdrawn / Cancelled'),
    )
    employee = models.OneToOneField('employees.Employee', on_delete=models.CASCADE, related_name='offboarding_workflow')
    notice_date = models.DateField()
    last_working_day = models.DateField()
    reason = models.CharField(max_length=30, choices=REASON_CHOICES, default='RESIGNATION')
    detailed_reason = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='INITIATED')
    handover_to = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='handed_over_responsibilities')
    is_eligible_for_rehire = models.BooleanField(default=True)

    def __str__(self):
        return f"Offboarding: {self.employee.full_name} (LWD: {self.last_working_day})"


class OffboardingClearance(TimeStampedModel):
    DEPT_CHOICES = (
        ('IT', 'IT Assets & System Accounts Deactivation'),
        ('FINANCE', 'Finance & Payroll Clearance (Loans / Advance)'),
        ('FACILITIES', 'Facilities ID Badge & Access Card Return'),
        ('HR', 'HR Exit Documentation & Statutory Forms'),
        ('DEPT', 'Departmental Knowledge Transfer & Project Handover'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending Clearance'),
        ('APPROVED', 'Approved & Cleared'),
        ('REJECTED', 'Issues Flagged / Deductions Required'),
    )
    offboarding = models.ForeignKey(EmployeeOffboarding, on_delete=models.CASCADE, related_name='clearances')
    department = models.CharField(max_length=20, choices=DEPT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cleared_by = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_clearances')
    cleared_at = models.DateTimeField(null=True, blank=True)
    recoverable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('offboarding', 'department')

    def __str__(self):
        return f"{self.get_department_display()} for {self.offboarding.employee.full_name}"
