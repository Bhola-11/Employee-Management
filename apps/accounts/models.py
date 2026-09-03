import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, StatusModel

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_super_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Role(TimeStampedModel, StatusModel):
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('ORG_ADMIN', 'Organization Admin'),
        ('HR_MANAGER', 'HR Manager'),
        ('HR_EXECUTIVE', 'HR Executive'),
        ('RECRUITER', 'Recruiter'),
        ('PAYROLL_MANAGER', 'Payroll Manager'),
        ('FINANCE_MANAGER', 'Finance Manager'),
        ('DEPT_MANAGER', 'Department Manager'),
        ('TEAM_LEAD', 'Team Lead'),
        ('EMPLOYEE', 'Employee'),
        ('TRAINING_MANAGER', 'Training Manager'),
        ('IT_ASSET_MANAGER', 'IT/Asset Manager'),
        ('SUPPORT_AGENT', 'Support Agent'),
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    is_system_role = models.BooleanField(default=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_roles'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class Permission(TimeStampedModel):
    MODULE_CHOICES = (
        ('accounts', 'Accounts & Auth'),
        ('organizations', 'Organizations & Structure'),
        ('employees', 'Employee Directory'),
        ('recruitment', 'Recruitment & ATS'),
        ('onboarding', 'Onboarding & Exit'),
        ('attendance', 'Time & Attendance'),
        ('shifts', 'Shifts & Rosters'),
        ('leave', 'Leave Management'),
        ('payroll', 'Payroll & Compensation'),
        ('benefits', 'Benefits & Insurance'),
        ('performance', 'Performance & Appraisals'),
        ('goals', 'Goals & OKRs'),
        ('training', 'Training & LMS'),
        ('assets', 'IT & Physical Assets'),
        ('documents', 'Document Vault'),
        ('expenses', 'Expenses & Travel'),
        ('helpdesk', 'HR Helpdesk'),
        ('reports', 'Reports & Analytics'),
        ('audit', 'Audit Logs'),
    )
    ACTION_CHOICES = (
        ('view', 'View'),
        ('create', 'Create'),
        ('edit', 'Edit / Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve / Reject'),
        ('export', 'Export Data'),
        ('admin', 'Full Administrative'),
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True) # e.g. employees.create
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['module', 'action']

    def __str__(self):
        return f'{self.module}.{self.action} - {self.name}'


class RolePermission(TimeStampedModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f'{self.role.code} -> {self.permission.code}'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_super_admin = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    active_role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_users'
    )
    two_factor_enabled = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, default='en')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['email']

    def __str__(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    def has_role(self, *role_codes):
        if self.is_superuser or self.is_super_admin:
            return True
        assigned_roles = set(self.role_assignments.values_list('role__code', flat=True))
        if self.active_role:
            assigned_roles.add(self.active_role.code)
        for code in role_codes:
            if code in assigned_roles:
                return True
        return False

    def has_module_perm(self, module, action='view'):
        if self.is_superuser or self.is_super_admin:
            return True
        perm_code = f'{module}.{action}'
        assigned_role_ids = self.role_assignments.values_list('role_id', flat=True)
        return RolePermission.objects.filter(
            role_id__in=assigned_role_ids,
            permission__code=perm_code
        ).exists()


class UserRoleAssignment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_assignments')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_assignments')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='user_role_assignments'
    )
    department = models.ForeignKey(
        'organizations.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role_assignments'
    )
    is_primary = models.BooleanField(default=False)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles_assigned_by_me'
    )

    class Meta:
        unique_together = ('user', 'role', 'organization')
        ordering = ['-is_primary', 'role__name']

    def __str__(self):
        return f'{self.user.email} -> {self.role.name} ({self.organization.code})'


class UserSessionLog(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_logs')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f'{self.user.email} from {self.ip_address} at {self.login_time}'
