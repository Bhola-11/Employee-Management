from django.db.models import Count, Q
from django.utils import timezone
from .models import Employee, EmployeeLifecycleTransition
from apps.core.utils import generate_employee_id

class EmployeeService:
    @staticmethod
    def generate_next_employee_id(org):
        count = Employee.objects.filter(organization=org).count() + 1
        return generate_employee_id(org.code, count)

    @staticmethod
    def transition_employee_status(employee, new_status, changed_by, reason, remarks=''):
        old_status = employee.employment_status
        if old_status == new_status:
            return None

        # Log transition
        transition = EmployeeLifecycleTransition.objects.create(
            employee=employee,
            from_status=old_status,
            to_status=new_status,
            changed_by=changed_by,
            reason=reason,
            remarks=remarks
        )

        employee.employment_status = new_status
        if new_status == 'CONFIRMED' and not employee.confirmation_date:
            employee.confirmation_date = timezone.now().date()
        employee.save(update_fields=['employment_status', 'confirmation_date'])
        
        return transition

    @staticmethod
    def get_org_tree(org):
        top_managers = Employee.objects.filter(
            organization=org,
            direct_manager__isnull=True,
            employment_status__in=['ACTIVE', 'CONFIRMED', 'PROBATION']
        ).select_related('designation', 'department')
        
        def build_node(emp):
            subs = emp.subordinates.filter(
                employment_status__in=['ACTIVE', 'CONFIRMED', 'PROBATION']
            ).select_related('designation', 'department')
            return {
                'id': str(emp.id),
                'name': emp.full_name,
                'designation': emp.designation.title if emp.designation else '',
                'department': emp.department.name if emp.department else '',
                'photo': emp.profile_photo.url if emp.profile_photo else '',
                'subordinates': [build_node(s) for s in subs]
            }

        return [build_node(m) for m in top_managers]
