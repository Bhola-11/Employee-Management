import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Course, CourseEnrollment, CourseModule
from .forms import CourseForm

@login_required
def learning_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    courses = Course.objects.filter(organization=org)
    my_enrollments = []
    if employee:
        my_enrollments = CourseEnrollment.objects.filter(employee=employee).select_related('course')
        
    return render(request, 'learning/dashboard.html', {
        'courses': courses,
        'my_enrollments': my_enrollments,
        'employee': employee
    })

@login_required
def course_detail_view(request, course_id):
    org = request.tenant_org
    course = get_object_or_404(Course, id=course_id, organization=org)
    modules = course.modules.all()
    employee = getattr(request.user, 'employee_profile', None)
    enrollment = None
    if employee:
        enrollment = CourseEnrollment.objects.filter(employee=employee, course=course).first()
    return render(request, 'learning/course_detail.html', {'course': course, 'modules': modules, 'enrollment': enrollment})

@login_required
def enroll_course_view(request, course_id):
    org = request.tenant_org
    course = get_object_or_404(Course, id=course_id, organization=org)
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required to enroll in courses.")
        return redirect('learning:dashboard')
        
    enr, created = CourseEnrollment.objects.get_or_create(
        employee=employee, course=course,
        defaults={'status': 'IN_PROGRESS', 'progress_percentage': 10}
    )
    messages.success(request, f"Enrolled in '{course.title}' successfully.")
    return redirect('learning:course_detail', course.id)
