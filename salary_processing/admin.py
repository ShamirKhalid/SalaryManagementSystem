# salary_processing/admin.py

from django.contrib import admin
from .models import SalaryRecord

admin.site.register(SalaryRecord)
