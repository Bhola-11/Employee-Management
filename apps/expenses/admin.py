from django.contrib import admin
from .models import ExpenseCategory, ExpenseClaim, ExpenseItem

admin.site.register(ExpenseCategory)
admin.site.register(ExpenseClaim)
admin.site.register(ExpenseItem)
