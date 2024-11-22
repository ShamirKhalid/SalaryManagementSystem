# SalaryManagement/dashboard/views.py

from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def employee_list(request):
    return render(request, 'dashboard/employee_list.html')

def salary_summary(request):
    return render(request, 'dashboard/salary_summary.html')
