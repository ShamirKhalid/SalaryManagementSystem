# employee_portal/admin.py

from django.contrib import admin
from .models import EmployeeReport

@admin.register(EmployeeReport)
class EmployeeReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'report_date', 'basic_salary', 'deductions', 'net_salary')
