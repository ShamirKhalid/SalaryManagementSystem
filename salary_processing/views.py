# salary_processing/views.py

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from settings_app.models import TaxRate, Allowance
from .forms import CalculateSalaryForm, ApproveSalaryForm, DisburseSalaryForm
from .models import SalaryRecord


def calculate_salaries(request):
    tax_rates = TaxRate.objects.all()
    allowances = Allowance.objects.all()

    if request.method == 'POST':
        form = CalculateSalaryForm(request.POST)
        if form.is_valid():
            salary_record = form.save(commit=False)
            employee = salary_record.employee
            month = salary_record.month

            # Check if a salary record already exists for this employee and month
            existing_record = SalaryRecord.objects.filter(employee=employee, month=month).first()
            if existing_record:
                messages.warning(request, 'Salary for this employee for the selected month has already been calculated.')
                return redirect('salary_details', pk=existing_record.pk)

            basic_salary = employee.salary

            # Calculate total allowances
            total_allowances = sum(allowance.amount for allowance in allowances)
            # Calculate total deductions based on tax rates
            total_deductions = sum((basic_salary * (tax.rate / 100)) for tax in tax_rates)

            salary_record.basic_salary = basic_salary
            salary_record.allowances = total_allowances
            salary_record.deductions = total_deductions
            salary_record.net_salary = basic_salary + total_allowances - total_deductions
            salary_record.save()

            return redirect('salary_details', pk=salary_record.pk)
    else:
        form = CalculateSalaryForm()

    context = {
        'form': form,
        'tax_rates': tax_rates,
        'allowances': allowances,
    }
    return render(request, 'salary_processing/calculate_salaries.html', context)

def approve_salaries(request, pk):
    salary_record = get_object_or_404(SalaryRecord, pk=pk)

    if request.method == 'POST':
        form = ApproveSalaryForm(request.POST, instance=salary_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary approved successfully.')
            return redirect('salary_details', pk=pk)
    else:
        form = ApproveSalaryForm(instance=salary_record)

    context = {
        'form': form,
        'salary_record': salary_record,
    }
    return render(request, 'salary_processing/approve_salaries.html', context)

def disburse_salary(request, pk):
    salary_record = get_object_or_404(SalaryRecord, pk=pk)
    employee = salary_record.employee

    if request.method == 'POST':
        form = DisburseSalaryForm(request.POST, instance=salary_record)
        if form.is_valid():
            # Dummy function to simulate bank transfer
            def process_payment(amount):
                # Logic to integrate with a bank API to process the payment
                return True  # Assume the payment is successful

            success = process_payment(salary_record.net_salary)

            if success:
                # Send confirmation email
                send_mail(
                    'Salary Disbursement Confirmation',
                    f'Dear {employee.first_name},\n\nYour salary of {salary_record.net_salary} has been disbursed to your bank account ({employee.bank_name}): {employee.bank_account_number}.\n\nBest regards,\nYour Company',
                    'ummasalarymanagementdisburser@gmail.com',
                    [employee.email],
                    fail_silently=False,
                )
                messages.success(request, 'Salary disbursed successfully.')
                return redirect('salary_details', pk=pk)
            else:
                messages.error(request, 'Salary disbursement failed.')
    else:
        form = DisburseSalaryForm(instance=salary_record)

    context = {
        'form': form,
        'salary_record': salary_record,
    }
    return render(request, 'salary_processing/disburse_salary.html', context)

def salary_details(request, pk):
    salary_record = get_object_or_404(SalaryRecord, pk=pk)
    salary_records = SalaryRecord.objects.filter(employee=salary_record.employee)
    context = {
        'salary_record': salary_record,
        'salary_records': salary_records,
    }
    return render(request, 'salary_processing/salary_details.html', context)
