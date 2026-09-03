from django.contrib import admin
from .models import PayrollCycle, PayrollRun, EmployeeSalaryStructure, Payslip

admin.site.register(PayrollCycle)
admin.site.register(PayrollRun)
admin.site.register(EmployeeSalaryStructure)
admin.site.register(Payslip)
