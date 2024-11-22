# reporting/models.py

from django.db import models
from employee_management.models import Employee  # Import Employee model

class Report(models.Model):
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    total_salaries = models.DecimalField(max_digits=15, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2)
    net_salaries = models.DecimalField(max_digits=15, decimal_places=2)
    employees = models.ManyToManyField(Employee)  # Link to Employee model

    def __str__(self):
        return f"{self.report_type} Report ({self.start_date} to {self.end_date})"
