from django.utils import timezone
from .models import Role, Permission, RolePermission, User, UserRoleAssignment, UserSessionLog
from apps.core.utils import get_client_ip

class RBACService:
    SYSTEM_ROLES = [
        ('SUPER_ADMIN', 'Super Admin', 'Full unrestricted platform access'),
        ('ORG_ADMIN', 'Organization Admin', 'Complete control over the organization'),
        ('HR_MANAGER', 'HR Manager', 'Manages employee lifecycle, policies, recruitment, and leaves'),
        ('HR_EXECUTIVE', 'HR Executive', 'Handles daily HR tasks, attendance, and record keeping'),
        ('RECRUITER', 'Recruiter', 'Manages job vacancies, candidates, and interview scheduling'),
        ('PAYROLL_MANAGER', 'Payroll Manager', 'Processes payroll structures, benefits, and salary releases'),
        ('FINANCE_MANAGER', 'Finance Manager', 'Approves expenses, budgets, and financial settlements'),
        ('DEPT_MANAGER', 'Department Manager', 'Manages department members, goals, and appraisals'),
        ('TEAM_LEAD', 'Team Lead', 'Supervises team shifts, task assignments, and reviews'),
        ('EMPLOYEE', 'Employee', 'Standard employee self-service portal'),
        ('TRAINING_MANAGER', 'Training Manager', 'Oversees courses, skill matrices, and certifications'),
        ('IT_ASSET_MANAGER', 'IT/Asset Manager', 'Manages hardware, software licenses, and equipment allocations'),
        ('SUPPORT_AGENT', 'Support Agent', 'Resolves HR helpdesk and internal support tickets'),
    ]

    @classmethod
    def initialize_system_roles(cls):
        created_count = 0
        for code, name, desc in cls.SYSTEM_ROLES:
            role, created = Role.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': desc, 'is_system_role': True}
            )
            if created:
                created_count += 1
        return created_count

    @classmethod
    def assign_role_to_user(cls, user, role_code, org, department=None, is_primary=True, assigned_by=None):
        role = Role.objects.get(code=role_code)
        if is_primary:
            UserRoleAssignment.objects.filter(user=user, organization=org).update(is_primary=False)
            user.active_role = role
            user.save(update_fields=['active_role'])
            
        assignment, created = UserRoleAssignment.objects.update_or_create(
            user=user,
            role=role,
            organization=org,
            defaults={
                'department': department,
                'is_primary': is_primary,
                'assigned_by': assigned_by
            }
        )
        return assignment

class AuthService:
    @staticmethod
    def log_user_session(request, user):
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', 'Unknown')
        session_key = request.session.session_key or ''
        
        user.last_login_ip = ip
        user.last_activity = timezone.now()
        user.save(update_fields=['last_login_ip', 'last_activity'])

        return UserSessionLog.objects.create(
            user=user,
            ip_address=ip,
            user_agent=ua,
            session_key=session_key,
            is_active=True
        )

    @staticmethod
    def close_user_session(request, user):
        session_key = request.session.session_key
        if session_key and user.is_authenticated:
            UserSessionLog.objects.filter(user=user, session_key=session_key, is_active=True).update(
                logout_time=timezone.now(),
                is_active=False
            )
