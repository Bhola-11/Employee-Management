from datetime import timedelta
from django.utils import timezone
from .models import EmployeeOnboarding, OnboardingTask, EmployeeOffboarding, OffboardingClearance
from apps.audit.services import AuditService

class OnboardingService:
    @staticmethod
    def instantiate_onboarding(onboarding_obj, user):
        if onboarding_obj.template:
            for task_tpl in onboarding_obj.template.task_templates.all():
                due = onboarding_obj.start_date + timedelta(days=task_tpl.due_day_offset)
                OnboardingTask.objects.create(
                    onboarding=onboarding_obj,
                    title=task_tpl.title,
                    category=task_tpl.category,
                    description=task_tpl.description,
                    due_date=due,
                    status='PENDING'
                )
        onboarding_obj.calculate_progress()
        AuditService.log_activity(
            organization=onboarding_obj.employee.organization,
            user=user,
            module='onboarding',
            action='CREATE',
            obj=onboarding_obj,
            description=f"Initialized onboarding workflow for {onboarding_obj.employee.full_name}"
        )
        return onboarding_obj

class OffboardingService:
    @staticmethod
    def initiate_offboarding(offboarding_obj, user):
        dept_clearances = ['IT', 'FINANCE', 'FACILITIES', 'HR', 'DEPT']
        for dept in dept_clearances:
            OffboardingClearance.objects.get_or_create(
                offboarding=offboarding_obj,
                department=dept,
                defaults={'status': 'PENDING'}
            )
        AuditService.log_activity(
            organization=offboarding_obj.employee.organization,
            user=user,
            module='offboarding',
            action='CREATE',
            obj=offboarding_obj,
            description=f"Initiated exit clearance workflow for {offboarding_obj.employee.full_name}"
        )
        return offboarding_obj
