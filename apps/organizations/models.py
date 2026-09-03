from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel, StatusModel

class Organization(TimeStampedModel, StatusModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True, default='Technology')
    tax_id = models.CharField(max_length=100, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    currency = models.CharField(max_length=10, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(max_length=20, default='YYYY-MM-DD')
    fiscal_year_start = models.PositiveSmallIntegerField(default=1)  # Month 1-12
    max_employees = models.PositiveIntegerField(default=5000)
    settings_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.code:
            self.code = self.name[:3].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.code})'


class Branch(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_headquarters = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='United States')
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    timezone = models.CharField(max_length=50, default='UTC')

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['-is_headquarters', 'name']
        verbose_name_plural = 'Branches'

    def __str__(self):
        hq = ' (HQ)' if self.is_headquarters else ''
        return f'{self.name}{hq} - {self.organization.code}'


class Department(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_departments')
    department_head = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='heading_departments')
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class Team(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    team_lead = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='led_teams')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.department.name}'


class JobLevel(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='job_levels')
    level_name = models.CharField(max_length=100) # e.g. Executive, Senior, Lead, Director
    rank_order = models.PositiveSmallIntegerField(default=1) # 1 to 10
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'level_name')
        ordering = ['rank_order']

    def __str__(self):
        return f'L{self.rank_order} - {self.level_name}'


class Designation(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='designations')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='designations')
    job_level = models.ForeignKey(JobLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name='designations')
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.code})'


class EmploymentType(TimeStampedModel, StatusModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employment_types')
    name = models.CharField(max_length=100) # Full-Time, Part-Time, Contract, Intern
    code = models.CharField(max_length=50)
    standard_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2, default=40.00)
    has_benefits = models.BooleanField(default=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class WorkLocation(TimeStampedModel, StatusModel):
    LOCATION_TYPES = (
        ('ON_SITE', 'On-Site Office'),
        ('REMOTE', 'Remote / Home'),
        ('HYBRID', 'Hybrid'),
        ('CLIENT_SITE', 'Client Site'),
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='work_locations')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='work_locations')
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='ON_SITE')
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    seating_capacity = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_location_type_display()})'


class ReportingHierarchy(TimeStampedModel):
    RELATION_TYPES = (
        ('PRIMARY', 'Primary Direct Manager'),
        ('MATRIX', 'Matrix / Dotted Line Manager'),
        ('FUNCTIONAL', 'Functional / Technical Lead'),
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='reporting_hierarchies')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='management_relations')
    manager = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='subordinate_relations')
    relationship_type = models.CharField(max_length=20, choices=RELATION_TYPES, default='PRIMARY')
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ['-effective_from']
        verbose_name_plural = 'Reporting Hierarchies'

    def __str__(self):
        return f'{self.employee} -> {self.manager} ({self.get_relationship_type_display()})'
