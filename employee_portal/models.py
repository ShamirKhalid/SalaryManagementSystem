# employee_portal/models.py
from django.db import models
from employee_management.models import Employee

class EmployeeReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.report_date}"

