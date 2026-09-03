from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveApplication

admin.site.register(LeaveType)
admin.site.register(LeaveBalance)
admin.site.register(LeaveApplication)
