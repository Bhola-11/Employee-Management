from django.contrib import admin
from .models import AttendanceRecord, AttendanceRegularization, MonthlyAttendanceSummary

admin.site.register(AttendanceRecord)
admin.site.register(AttendanceRegularization)
admin.site.register(MonthlyAttendanceSummary)
