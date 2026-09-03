from django.contrib import admin
from .models import BenefitPlan, EmployeeBenefitEnrollment

admin.site.register(BenefitPlan)
admin.site.register(EmployeeBenefitEnrollment)
