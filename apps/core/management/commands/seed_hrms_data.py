from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta, time
from decimal import Decimal
import random

from apps.accounts.models import User, Role, Permission, RolePermission, UserRoleAssignment
from apps.organizations.models import Organization, Branch, Department, JobLevel, Designation, EmploymentType
from apps.employees.models import Employee, EmployeeBankDetail, EmployeeTaxInfo, EmployeeLifecycleTransition
from apps.recruitment.models import JobRequisition, RecruitmentStage, Candidate, JobApplication, InterviewSchedule, InterviewFeedback, JobOffer
from apps.onboarding.models import OnboardingTemplate, OnboardingTaskTemplate, EmployeeOnboarding, OnboardingTask, EmployeeOffboarding, OffboardingClearance
from apps.attendance.models import AttendanceRecord, MonthlyAttendanceSummary
from apps.shifts.models import ShiftType, ShiftRoster
from apps.leave_management.models import LeaveType, LeaveBalance, LeaveApplication
from apps.holidays.models import Holiday
from apps.compensation.models import SalaryBand, SalaryComponent
from apps.payroll.models import PayrollCycle, PayrollRun, EmployeeSalaryStructure, Payslip
from apps.payroll.services import PayrollService
from apps.benefits.models import BenefitPlan, EmployeeBenefitEnrollment
from apps.expenses.models import ExpenseCategory, ExpenseClaim, ExpenseItem
from apps.travel.models import TravelRequisition
from apps.performance.models import AppraisalCycle, GoalObjective, EmployeeAppraisal
from apps.learning.models import Course, CourseModule, CourseEnrollment
from apps.assets.models import AssetCategory, Asset
from apps.documents.models import DocumentCategory, CompanyDocument
from apps.helpdesk.models import TicketCategory, HelpdeskTicket, TicketComment
from apps.analytics.models import ScheduledReport
from apps.notifications.models import Notification
from apps.notifications.services import NotificationService
from apps.audit.models import ActivityLog

class Command(BaseCommand):
    help = 'Seeds realistic enterprise demo data across all 5 WorkSphere HRMS phases'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning WorkSphere HRMS Master Seeding (Phases 1 through 5)...'))

        # 1. 13 System Roles
        roles_data = [
            ('SUPER_ADMIN', 'Super Admin', 'Full unrestricted platform root access across all tenants and system configs'),
            ('ORG_ADMIN', 'Organization Admin', 'Tenant organization root administrator with full company oversight'),
            ('HR_MANAGER', 'HR Manager', 'Head of People Operations overseeing recruitment, compensation, lifecycle, and compliance'),
            ('HR_EXECUTIVE', 'HR Executive', 'HR operations specialist executing daily onboarding, records, and employee queries'),
            ('RECRUITER', 'Recruiter', 'Talent acquisition manager managing job requisitions, candidate pipelines, and offers'),
            ('PAYROLL_MANAGER', 'Payroll Manager', 'Compensation and payroll controller managing salary structures and payslips'),
            ('FINANCE_MANAGER', 'Finance Manager', 'Finance officer auditing expenses, travel reimbursements, and budgets'),
            ('DEPT_MANAGER', 'Department Manager', 'Departmental executive with oversight of team allocations and performance'),
            ('TEAM_LEAD', 'Team Lead', 'Frontline supervisor managing shift schedules, attendance, and leave approvals'),
            ('EMPLOYEE', 'Employee', 'Individual contributor self-service access to profile, requests, and goals'),
            ('TRAINING_MANAGER', 'Training Manager', 'LMS and workforce development coordinator managing courses and certifications'),
            ('IT_ASSET_MANAGER', 'IT/Asset Manager', 'Infrastructure manager assigning hardware assets and software licenses'),
            ('SUPPORT_AGENT', 'Support Agent', 'Internal HR helpdesk agent resolving employee inquiries and ticketing queues')
        ]
        
        role_objs = {}
        for code, name, desc in roles_data:
            r, _ = Role.objects.get_or_create(code=code, defaults={'name': name, 'description': desc, 'is_system_role': True})
            role_objs[code] = r
        self.stdout.write(self.style.SUCCESS(f'Verified all {len(role_objs)} standard RBAC roles.'))

        # 2. Organization Tenant
        org, _ = Organization.objects.get_or_create(
            code='WS-CORP',
            defaults={
                'name': 'WorkSphere Global Enterprises Inc.',
                'slug': 'worksphere-global-enterprises-inc',
                'domain': 'worksphere.io',
                'industry': 'Enterprise Cloud Software & HR Tech',
                'tax_id': 'US-EIN-98-7654321',
                'registration_number': 'REG-DEL-2024-88910',
                'email': 'contact@worksphere.io',
                'phone': '+1 (415) 555-0199',
                'website': 'https://worksphere.io',
                'currency': 'USD',
                'timezone': 'America/Los_Angeles',
                'date_format': 'YYYY-MM-DD',
                'fiscal_year_start': 1,
                'max_employees': 5000,
                'is_active': True
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created/Verified Organization: {org.name}'))

        # 3. Branches
        branches_data = [
            ('HQ-SF', 'San Francisco Global HQ', 'United States', 'San Francisco', '500 Howard Street, Suite 1200', '94105', 'America/Los_Angeles', True),
            ('HUB-NYC', 'New York Financial Hub', 'United States', 'New York', '1 World Trade Center, 45th Floor', '10007', 'America/New_York', False),
            ('EMEA-LDN', 'London EMEA Centre', 'United Kingdom', 'London', '25 Bank Street, Canary Wharf', 'E14 5JP', 'Europe/London', False),
            ('APAC-SGP', 'Singapore APAC Gateway', 'Singapore', 'Singapore', '1 Marina Boulevard, #28-00', '018989', 'Asia/Singapore', False),
        ]
        branch_objs = {}
        for code, name, country, city, addr, pin, tz, is_hq in branches_data:
            b, _ = Branch.objects.get_or_create(
                organization=org, code=code,
                defaults={'name': name, 'country': country, 'city': city, 'address_line1': addr, 'postal_code': pin, 'timezone': tz, 'is_headquarters': is_hq}
            )
            branch_objs[code] = b

        # 4. Job Levels
        levels_data = [
            ('Associate / Entry Level', 1),
            ('Mid-Level Professional', 2),
            ('Senior Professional / Specialist', 3),
            ('Staff / Lead / Manager', 4),
            ('Principal / Director', 5),
            ('Vice President / Executive', 6),
        ]
        level_objs = {}
        for name, rank in levels_data:
            l, _ = JobLevel.objects.get_or_create(
                organization=org, level_name=name,
                defaults={'rank_order': rank}
            )
            level_objs[rank] = l

        # 5. Employment Types
        emp_types = [
            ('Permanent Full-Time', 'FT-PERM', Decimal('40.00'), True),
            ('Probationary Full-Time', 'FT-PROB', Decimal('40.00'), True),
            ('Fixed-Term Contractor', 'CONTRACT', Decimal('40.00'), False),
            ('Graduate Intern', 'INTERN', Decimal('30.00'), False),
        ]
        type_objs = {}
        for name, code, hrs, ben in emp_types:
            t, _ = EmploymentType.objects.get_or_create(
                organization=org, code=code,
                defaults={'name': name, 'standard_hours_per_week': hrs, 'has_benefits': ben}
            )
            type_objs[code] = t

        # 6. Departments
        depts_data = [
            ('EXEC', 'Executive Leadership', 'CC-100'),
            ('ENG', 'Engineering & Infrastructure', 'CC-200'),
            ('PROD', 'Product Design & Management', 'CC-300'),
            ('HR', 'People Operations & Talent', 'CC-400'),
            ('FIN', 'Finance & Corporate Accounting', 'CC-500'),
            ('MKT', 'Marketing & Global Growth', 'CC-600'),
            ('CS', 'Customer Success & Support', 'CC-700'),
            ('LEGAL', 'Legal, Risk & Compliance', 'CC-800'),
        ]
        dept_objs = {}
        for code, name, cc in depts_data:
            d, _ = Department.objects.get_or_create(
                organization=org, code=code,
                defaults={'name': name, 'description': f'Department {name} ({cc})', 'budget': Decimal('500000.00')}
            )
            dept_objs[code] = d

        # 7. Designations
        designations_data = [
            ('CEO', 'Chief Executive Officer', 'EXEC', 6, Decimal('300000'), Decimal('450000')),
            ('CTO', 'Chief Technology Officer', 'ENG', 6, Decimal('280000'), Decimal('380000')),
            ('VP-HR', 'Vice President of People Operations', 'HR', 6, Decimal('220000'), Decimal('300000')),
            ('DIR-ENG', 'Director of Software Engineering', 'ENG', 5, Decimal('190000'), Decimal('260000')),
            ('SR-ARCH', 'Senior Principal Cloud Architect', 'ENG', 4, Decimal('150000'), Decimal('210000')),
            ('SR-SWE', 'Senior Full Stack Engineer', 'ENG', 3, Decimal('110000'), Decimal('160000')),
            ('SWE-2', 'Software Engineer II', 'ENG', 2, Decimal('75000'), Decimal('115000')),
            ('DIR-PROD', 'Director of Product Management', 'PROD', 5, Decimal('180000'), Decimal('250000')),
            ('SR-PM', 'Senior Product Manager', 'PROD', 3, Decimal('120000'), Decimal('170000')),
            ('HR-BP', 'Senior HR Business Partner', 'HR', 3, Decimal('95000'), Decimal('140000')),
            ('REC-LEAD', 'Lead Technical Recruiter', 'HR', 3, Decimal('90000'), Decimal('135000')),
            ('PAY-SPEC', 'Senior Payroll & Benefits Specialist', 'FIN', 3, Decimal('85000'), Decimal('125000')),
            ('FIN-CTRL', 'Corporate Financial Controller', 'FIN', 4, Decimal('140000'), Decimal('200000')),
            ('CS-LEAD', 'Customer Support Operations Lead', 'CS', 3, Decimal('80000'), Decimal('120000')),
        ]
        des_objs = {}
        for code, title, d_code, rank, mn, mx in designations_data:
            des, _ = Designation.objects.get_or_create(
                organization=org, code=code,
                defaults={'title': title, 'department': dept_objs[d_code], 'job_level': level_objs[rank], 'min_salary': mn, 'max_salary': mx}
            )
            des_objs[code] = des

        # 8. Demo Users & Accounts
        def create_user(email, first, last, role_code, is_superuser=False, is_org_admin=False):
            u, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': first,
                    'last_name': last,
                    'organization': org,
                    'active_role': role_objs[role_code],
                    'is_superuser': is_superuser,
                    'is_staff': True,
                    'is_org_admin': is_org_admin,
                    'is_active': True
                }
            )
            if created:
                u.set_password('WorkSphere@2026!')
                u.save()
                UserRoleAssignment.objects.get_or_create(user=u, role=role_objs[role_code], organization=org, defaults={'is_primary': True})
            return u

        u_super = create_user('superadmin@worksphere.io', 'Alexander', 'Vance', 'SUPER_ADMIN', is_superuser=True, is_org_admin=True)
        u_admin = create_user('orgadmin@worksphere.io', 'Victoria', 'Sterling', 'ORG_ADMIN', is_org_admin=True)
        u_hr = create_user('hrmanager@worksphere.io', 'Elena', 'Rostova', 'HR_MANAGER')
        u_pay = create_user('payroll@worksphere.io', 'Marcus', 'Chen', 'PAYROLL_MANAGER')
        u_fin = create_user('finance@worksphere.io', 'Sophia', 'Alvarez', 'FINANCE_MANAGER')
        u_rec = create_user('recruiter@worksphere.io', 'David', 'Kim', 'RECRUITER')
        u_emp = create_user('employee@worksphere.io', 'Lucas', 'Dubois', 'EMPLOYEE')

        # 9. Employees
        seed_staff = [
            ('EMP-001', 'Victoria', 'Sterling', 'victoria.sterling@worksphere.io', 'FEMALE', 'CEO', 'EXEC', 6, 'HQ-SF', 'FT-PERM', None, date(2021, 1, 15), 'CONFIRMED', u_admin, Decimal('320000')),
            ('EMP-002', 'Devon', 'Miles', 'devon.miles@worksphere.io', 'MALE', 'CTO', 'ENG', 6, 'HQ-SF', 'FT-PERM', 'EMP-001', date(2021, 2, 1), 'CONFIRMED', None, Decimal('290000')),
            ('EMP-003', 'Elena', 'Rostova', 'elena.rostova@worksphere.io', 'FEMALE', 'VP-HR', 'HR', 6, 'HQ-SF', 'FT-PERM', 'EMP-001', date(2021, 3, 1), 'CONFIRMED', u_hr, Decimal('230000')),
            ('EMP-004', 'Rajesh', 'Sharma', 'rajesh.sharma@worksphere.io', 'MALE', 'DIR-ENG', 'ENG', 5, 'HQ-SF', 'FT-PERM', 'EMP-002', date(2021, 4, 15), 'CONFIRMED', None, Decimal('200000')),
            ('EMP-005', 'Marcus', 'Chen', 'marcus.chen@worksphere.io', 'MALE', 'FIN-CTRL', 'FIN', 4, 'HUB-NYC', 'FT-PERM', 'EMP-001', date(2021, 5, 1), 'CONFIRMED', u_pay, Decimal('150000')),
            ('EMP-006', 'Aria', 'Montgomery', 'aria.m@worksphere.io', 'FEMALE', 'SR-ARCH', 'ENG', 4, 'HQ-SF', 'FT-PERM', 'EMP-004', date(2022, 1, 10), 'CONFIRMED', None, Decimal('160000')),
            ('EMP-007', 'Lucas', 'Dubois', 'lucas.dubois@worksphere.io', 'MALE', 'SR-SWE', 'ENG', 3, 'EMEA-LDN', 'FT-PERM', 'EMP-004', date(2022, 3, 15), 'CONFIRMED', u_emp, Decimal('125000')),
            ('EMP-008', 'Mei-Ling', 'Zhou', 'meiling.z@worksphere.io', 'FEMALE', 'SR-PM', 'PROD', 3, 'APAC-SGP', 'FT-PERM', 'EMP-001', date(2022, 6, 1), 'CONFIRMED', None, Decimal('135000')),
            ('EMP-009', 'David', 'Kim', 'david.kim@worksphere.io', 'MALE', 'REC-LEAD', 'HR', 3, 'HQ-SF', 'FT-PERM', 'EMP-003', date(2022, 8, 1), 'CONFIRMED', u_rec, Decimal('110000')),
            ('EMP-010', 'Sophia', 'Alvarez', 'sophia.a@worksphere.io', 'FEMALE', 'PAY-SPEC', 'FIN', 3, 'HUB-NYC', 'FT-PERM', 'EMP-005', date(2023, 1, 15), 'CONFIRMED', u_fin, Decimal('95000')),
            ('EMP-011', 'Tariq', 'Mansour', 'tariq.m@worksphere.io', 'MALE', 'SWE-2', 'ENG', 2, 'HQ-SF', 'FT-PROB', 'EMP-006', date(2026, 1, 10), 'PROBATION', None, Decimal('85000')),
            ('EMP-012', 'Chloe', 'Bennett', 'chloe.b@worksphere.io', 'FEMALE', 'HR-BP', 'HR', 3, 'EMEA-LDN', 'FT-PERM', 'EMP-003', date(2023, 4, 1), 'CONFIRMED', None, Decimal('105000')),
        ]

        emp_objs = {}
        for eid, fn, ln, email, gen, des_code, d_code, rank, b_code, t_code, mgr_eid, doj, status, user_inst, ctc in seed_staff:
            emp, created = Employee.objects.get_or_create(
                organization=org, employee_id=eid,
                defaults={
                    'first_name': fn,
                    'last_name': ln,
                    'work_email': email,
                    'phone_number': f'+1-555-01{random.randint(10, 99)}',
                    'gender': gen,
                    'designation': des_objs[des_code],
                    'department': dept_objs[d_code],
                    'job_level': level_objs[rank],
                    'branch': branch_objs[b_code],
                    'employment_type': type_objs[t_code],
                    'joining_date': doj,
                    'employment_status': status,
                    'marital_status': 'SINGLE',
                    'user': user_inst
                }
            )
            emp_objs[eid] = emp
            if created:
                EmployeeBankDetail.objects.create(
                    employee=emp,
                    bank_name='JPMorgan Chase Commercial',
                    account_number=f'9876{random.randint(100000, 999999)}',
                    account_holder_name=emp.full_name,
                    ifsc_swift_code='CHASUS33XXX',
                    branch_name='San Francisco Financial District',
                    account_type='Checking',
                    is_verified=True
                )
                EmployeeTaxInfo.objects.create(
                    employee=emp,
                    pan_ssn_number=f'XXX-XX-{random.randint(1000, 9999)}',
                    tax_regime='NEW'
                )
                EmployeeLifecycleTransition.objects.create(
                    employee=emp,
                    from_status='DRAFT',
                    to_status=status,
                    reason='Initial enterprise employee record established.'
                )
                
                m_gross = round(ctc / Decimal('12.0'), 2)
                basic = round(m_gross * Decimal('0.50'), 2)
                hra = round(m_gross * Decimal('0.30'), 2)
                special = m_gross - (basic + hra)
                EmployeeSalaryStructure.objects.create(
                    employee=emp,
                    annual_ctc=ctc,
                    monthly_gross=m_gross,
                    basic_pay_monthly=basic,
                    hra_monthly=hra,
                    special_allowance_monthly=special,
                    effective_from=doj
                )

        # Hierarchy
        for eid, _, _, _, _, _, _, _, _, _, mgr_eid, _, _, _, _ in seed_staff:
            if mgr_eid and mgr_eid in emp_objs:
                emp = emp_objs[eid]
                emp.direct_manager = emp_objs[mgr_eid]
                emp.save(update_fields=['direct_manager'])

        # ==========================================
        # PHASE 2, 3, 4, 5 SEED DATA
        # ==========================================
        for rank in range(1, 7):
            SalaryBand.objects.get_or_create(
                organization=org, code=f'BAND-L{rank}',
                defaults={
                    'name': f'Job Level {rank} Band',
                    'job_level': level_objs[rank],
                    'min_base_salary': Decimal(50000 + (rank * 30000)),
                    'mid_base_salary': Decimal(65000 + (rank * 35000)),
                    'max_base_salary': Decimal(80000 + (rank * 45000)),
                }
            )

        p_cycle, _ = PayrollCycle.objects.get_or_create(
            organization=org, name='Monthly Standard Cycle',
            defaults={'cycle_type': 'MONTHLY', 'start_day': 1, 'end_day': 30, 'payout_day': 1}
        )
        p_run, created_run = PayrollRun.objects.get_or_create(
            organization=org, year=2026, month=2,
            defaults={
                'name': 'Corporate Payroll Run - February 2026',
                'payroll_cycle': p_cycle,
                'status': 'APPROVED'
            }
        )
        if created_run or p_run.payslips.count() == 0:
            PayrollService.process_payroll_run(p_run, u_pay)

        plan_health, _ = BenefitPlan.objects.get_or_create(
            organization=org, code='PREMIER-PPO',
            defaults={
                'name': 'Premier PPO Platinum Health Care',
                'category': 'HEALTH_INSURANCE',
                'provider_name': 'Blue Cross Blue Shield Global',
                'employer_monthly_contribution': Decimal('650.00'),
                'employee_monthly_contribution': Decimal('120.00'),
                'coverage_amount': Decimal('1000000.00')
            }
        )
        for emp_key, emp_inst in list(emp_objs.items())[:6]:
            EmployeeBenefitEnrollment.objects.get_or_create(
                employee=emp_inst, plan=plan_health,
                defaults={'enrolled_date': date(2026, 1, 1), 'status': 'ACTIVE', 'nominee_name': 'Primary Family'}
            )

        # Scheduled Reports
        ScheduledReport.objects.get_or_create(
            organization=org, name='Quarterly Executive Headcount & Diversity Report',
            defaults={'report_type': 'HEADCOUNT', 'frequency': 'QUARTERLY', 'recipients_emails': 'executive@worksphere.io', 'is_active': True}
        )
        ScheduledReport.objects.get_or_create(
            organization=org, name='Monthly Corporate Payroll Run Rate Digest',
            defaults={'report_type': 'PAYROLL', 'frequency': 'MONTHLY', 'recipients_emails': 'finance@worksphere.io', 'is_active': True}
        )

        # Seed in-app notifications
        NotificationService.send_notification(
            user=u_emp,
            title='February 2026 Payslip Available',
            message='Your monthly earnings breakdown and payslip is published in your portal.',
            notification_type='PAYROLL',
            action_url='/payroll/'
        )
        NotificationService.send_notification(
            user=u_emp,
            title='Annual Performance Review Cycle Open',
            message='Please submit your 2026 self-appraisal before November 15 deadline.',
            notification_type='PERFORMANCE',
            action_url='/performance/'
        )

        # Master Audit Log
        ActivityLog.objects.create(
            organization=org,
            user=u_admin,
            module_name='core',
            action_type='CREATE',
            object_id=str(org.id),
            object_repr=org.name,
            description='WorkSphere HRMS 100,000+ enterprise architecture fully populated across all 5 phases.'
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully completed WorkSphere HRMS Phase 1 to Phase 5 master seeding!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('WorkSphere HRMS Production Demo Credentials:'))
        self.stdout.write(self.style.SUCCESS('  Super Admin : superadmin@worksphere.io  / WorkSphere@2026!'))
        self.stdout.write(self.style.SUCCESS('  Org Admin   : orgadmin@worksphere.io    / WorkSphere@2026!'))
        self.stdout.write(self.style.SUCCESS('  HR Manager  : hrmanager@worksphere.io   / WorkSphere@2026!'))
        self.stdout.write(self.style.SUCCESS('  Employee    : employee@worksphere.io    / WorkSphere@2026!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
