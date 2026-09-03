from decimal import Decimal
import uuid
from .models import PayrollRun, Payslip, EmployeeSalaryStructure
from apps.employees.models import Employee
from apps.audit.services import AuditService

class PayrollService:
    @staticmethod
    def process_payroll_run(payroll_run, user=None):
        org = payroll_run.organization
        employees = Employee.objects.filter(organization=org, employment_status__in=['ACTIVE', 'PROBATION', 'CONFIRMED'])
        
        total_gross = Decimal('0.00')
        total_ded = Decimal('0.00')
        total_net = Decimal('0.00')
        slips_created = 0
        
        for emp in employees:
            struct = getattr(emp, 'salary_structure', None)
            if not struct:
                # Default baseline if no explicit structure
                basic = Decimal('5000.00')
                hra = Decimal('2000.00')
                special = Decimal('1000.00')
            else:
                basic = struct.basic_pay_monthly
                hra = struct.hra_monthly
                special = struct.special_allowance_monthly
                
            gross = basic + hra + special
            tax = round(gross * Decimal('0.15'), 2)
            pf = round(basic * Decimal('0.06'), 2)
            deductions = tax + pf
            net = gross - deductions
            
            ps_num = f"PAY-{payroll_run.year}-{payroll_run.month:02d}-{emp.employee_id}"
            Payslip.objects.update_or_create(
                payroll_run=payroll_run,
                employee=emp,
                defaults={
                    'payslip_number': ps_num,
                    'basic_salary': basic,
                    'house_rent_allowance': hra,
                    'special_allowance': special,
                    'gross_earnings': gross,
                    'income_tax_deduction': tax,
                    'provident_fund_deduction': pf,
                    'total_deductions': deductions,
                    'net_salary': net,
                    'status': 'GENERATED',
                    'bank_account_masked': 'XXXX-XXXX-8899'
                }
            )
            total_gross += gross
            total_ded += deductions
            total_net += net
            slips_created += 1
            
        payroll_run.total_employees_count = slips_created
        payroll_run.total_gross_pay = total_gross
        payroll_run.total_deductions = total_ded
        payroll_run.total_net_pay = total_net
        payroll_run.status = 'UNDER_REVIEW'
        payroll_run.save()
        
        AuditService.log_activity(
            organization=org,
            user=user,
            module='payroll',
            action='CREATE',
            obj=payroll_run,
            description=f"Executed payroll run for {payroll_run.month}/{payroll_run.year} - {slips_created} payslips generated."
        )
        return payroll_run
