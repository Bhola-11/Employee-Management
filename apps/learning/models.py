from django.db import models
from apps.core.models import TimeStampedModel, StatusModel

class Course(TimeStampedModel, StatusModel):
    LEVEL_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced / Expert'),
    )
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255) # e.g. Cybersecurity Essentials, Enterprise Leadership, Cloud Architecture
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=100) # Compliance, Technical, Leadership, Security
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='INTERMEDIATE')
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=4.0)
    instructor_name = models.CharField(max_length=150, default='WorkSphere Academy')
    description = models.TextField()
    is_mandatory = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='courses/', null=True, blank=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.title} ({self.category})"


class CourseModule(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=1)
    content_text = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class CourseEnrollment(TimeStampedModel):
    STATUS_CHOICES = (
        ('ENROLLED', 'Enrolled / Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed & Certified'),
    )
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')
    progress_percentage = models.PositiveSmallIntegerField(default=0)
    certificate_id = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('employee', 'course')
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.employee.full_name} -> {self.course.title} ({self.progress_percentage}%)"
