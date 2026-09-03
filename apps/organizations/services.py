from django.db.models import Count
from .models import Organization, Department, Branch, Designation

class OrganizationService:
    @staticmethod
    def get_organization_overview(org):
        departments = Department.objects.filter(organization=org, is_active=True).annotate(
            headcount=Count('employees')
        )
        branches = Branch.objects.filter(organization=org, is_active=True).annotate(
            dept_count=Count('departments')
        )
        designations = Designation.objects.filter(organization=org, is_active=True).annotate(
            emp_count=Count('employees')
        )
        return {
            'organization': org,
            'departments': departments,
            'branches': branches,
            'designations': designations,
            'total_depts': departments.count(),
            'total_branches': branches.count(),
        }

class HierarchyService:
    @staticmethod
    def build_department_tree(org):
        roots = Department.objects.filter(organization=org, parent_department__isnull=True).prefetch_related('sub_departments')
        tree = []
        for r in roots:
            tree.append({
                'dept': r,
                'children': r.sub_departments.all(),
                'headcount': r.employees.count()
            })
        return tree
