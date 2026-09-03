from django.contrib import admin
from .models import Course, CourseModule, CourseEnrollment

admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(CourseEnrollment)
