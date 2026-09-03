from django.contrib import admin
from .models import OnboardingTemplate, OnboardingTaskTemplate, EmployeeOnboarding, OnboardingTask, EmployeeOffboarding, OffboardingClearance

admin.site.register(OnboardingTemplate)
admin.site.register(OnboardingTaskTemplate)
admin.site.register(EmployeeOnboarding)
admin.site.register(OnboardingTask)
admin.site.register(EmployeeOffboarding)
admin.site.register(OffboardingClearance)
