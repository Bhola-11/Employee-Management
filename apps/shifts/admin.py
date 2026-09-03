from django.contrib import admin
from .models import ShiftType, ShiftRoster, ShiftSwapRequest

admin.site.register(ShiftType)
admin.site.register(ShiftRoster)
admin.site.register(ShiftSwapRequest)
