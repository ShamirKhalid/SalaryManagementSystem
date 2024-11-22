# salary_processing/models.py

from django.db import models
from employee_management.models import Employee

class SalaryRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'month')  # Ensure no duplicate salary records for the same month

    def __str__(self):
        return f"Salary for {self.employee} - {self.month.strftime('%B %Y')}"

    @classmethod
    def get_employee_salary_records(cls, employee):
        return cls.objects.filter(employee=employee)
