from decimal import Decimal
from django.db.models import Count, Sum, Avg
from apps.employees.models import Employee
from apps.organizations.models import Department, Branch
from apps.payroll.models import PayrollRun, Payslip
from apps.attendance.models import AttendanceRecord
from apps.leave_management.models import LeaveApplication
from apps.recruitment.models import JobRequisition, JobApplication

class AnalyticsService:
    @staticmethod
    def get_executive_summary(organization):
        total_employees = Employee.objects.filter(organization=organization, employment_status__in=['ACTIVE', 'PROBATION', 'CONFIRMED']).count()
        total_depts = Department.objects.filter(organization=organization).count()
        total_branches = Branch.objects.filter(organization=organization).count()
        
        # Department headcount breakdown
        dept_breakdown = list(
            Department.objects.filter(organization=organization)
            .annotate(headcount=Count('employees'))
            .values('name', 'headcount')
        )
        
        # Gender diversity
        gender_stats = list(
            Employee.objects.filter(organization=organization)
            .values('gender')
            .annotate(count=Count('id'))
        )
        
        # Payroll trends
        payroll_runs = list(
            PayrollRun.objects.filter(organization=organization)
            .order_by('-year', '-month')[:6]
            .values('year', 'month', 'total_gross_pay', 'total_net_pay', 'total_deductions')
        )
        
        # Recruitment Funnel
        open_jobs = JobRequisition.objects.filter(organization=organization, status='OPEN').count()
        active_candidates = JobApplication.objects.filter(requisition__organization=organization).exclude(status__in=['HIRED', 'REJECTED', 'WITHDRAWN']).count()
        hired_total = JobApplication.objects.filter(requisition__organization=organization, status='HIRED').count()
        
        return {
            'total_headcount': total_employees,
            'total_departments': total_depts,
            'total_branches': total_branches,
            'dept_breakdown': dept_breakdown,
            'gender_stats': gender_stats,
            'payroll_trends': payroll_runs,
            'open_jobs': open_jobs,
            'active_candidates': active_candidates,
            'hired_total': hired_total,
        }
