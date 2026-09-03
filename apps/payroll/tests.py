from django.test import TestCase
from datetime import date
from decimal import Decimal
from apps.organizations.models import Organization, Department
from apps.employees.models import Employee
from apps.payroll.models import PayrollCycle, PayrollRun, EmployeeSalaryStructure, Payslip
from apps.payroll.services import PayrollService

class PayrollProcessingTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='PayCorp Global', code='PCG')
        self.dept = Department.objects.create(organization=self.org, name='FinTech', code='FT')
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-PAY-01', first_name='Satoshi', last_name='Nakamoto',
            work_email='satoshi@paycorp.com', phone_number='+1-555-0000', department=self.dept,
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.cycle = PayrollCycle.objects.create(organization=self.org, name='Monthly Standard', cycle_type='MONTHLY')
        self.struct = EmployeeSalaryStructure.objects.create(
            employee=self.emp, annual_ctc=Decimal('120000.00'), monthly_gross=Decimal('10000.00'),
            basic_pay_monthly=Decimal('6000.00'), hra_monthly=Decimal('2500.00'), special_allowance_monthly=Decimal('1500.00'),
            effective_from=date(2025, 1, 1)
        )

    def test_payroll_run_and_payslip_generation(self):
        run = PayrollRun.objects.create(
            organization=self.org, payroll_cycle=self.cycle, name='March 2026 Payroll',
            year=2026, month=3
        )
        PayrollService.process_payroll_run(run)
        
        self.assertEqual(run.total_employees_count, 1)
        self.assertEqual(run.payslips.count(), 1)
        
        ps = run.payslips.first()
        self.assertEqual(ps.basic_salary, Decimal('6000.00'))
        self.assertEqual(ps.gross_earnings, Decimal('10000.00'))
        # 15% tax on 10000 = 1500; 6% pf on 6000 = 360; total ded = 1860; net = 8140
        self.assertEqual(ps.income_tax_deduction, Decimal('1500.00'))
        self.assertEqual(ps.provident_fund_deduction, Decimal('360.00'))
        self.assertEqual(ps.total_deductions, Decimal('1860.00'))
        self.assertEqual(ps.net_salary, Decimal('8140.00'))
