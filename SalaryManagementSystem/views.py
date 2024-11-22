# SalaryManagementSystem/views.py
from django.shortcuts import render
from salary_processing.models import SalaryRecord

def index(request):
    salary_records = SalaryRecord.objects.all()
    context = {
        'salary_records': salary_records,
    }
    return render(request, 'index.html', context)
