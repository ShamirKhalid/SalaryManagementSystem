import base64
import io
import os
import shutil
import tempfile

import matplotlib.pyplot as plt
import pandas as pd
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from weasyprint import HTML

from employee_management.models import Employee
from salary_processing.models import SalaryRecord
from .forms import GenerateReportForm
from .models import Report


def generate_report(request):
    if request.method == 'POST':
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            salary_records = SalaryRecord.objects.filter(month__range=[start_date, end_date])

            # Get distinct employees
            employee_ids = salary_records.values_list('employee_id', flat=True).distinct()
            employees = Employee.objects.filter(id__in=employee_ids)

            total_salaries = salary_records.aggregate(total=Sum('basic_salary'))['total']
            total_deductions = salary_records.aggregate(total=Sum('deductions'))['total']
            net_salaries = salary_records.aggregate(total=Sum('net_salary'))['total']

            report = Report.objects.create(
                report_type=report_type,
                start_date=start_date,
                end_date=end_date,
                total_salaries=total_salaries,
                total_deductions=total_deductions,
                net_salaries=net_salaries
            )
            report.employees.set(employees)  # Save employee details to the report

            return redirect('view_report', pk=report.pk)
    else:
        form = GenerateReportForm()

    return render(request, 'reporting/generate_report.html', {'form': form})


def report_list(request):
    reports = Report.objects.all()
    return render(request, 'reporting/report_list.html', {'reports': reports})


def view_report(request, pk):
    report = Report.objects.get(pk=pk)
    salary_records = SalaryRecord.objects.filter(month__range=[report.start_date, report.end_date])
    employees = report.employees.all()

    # Generate salary distribution chart
    salaries = salary_records.values_list('basic_salary', flat=True)
    plt.figure(figsize=(10, 5))
    plt.hist(salaries, bins=10)
    plt.title('Salary Distribution')
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    chart = io.BytesIO()
    plt.savefig(chart, format='png')
    chart.seek(0)
    chart_png = base64.b64encode(chart.getvalue()).decode('utf-8')
    plt.close()

    # Generate deductions over time graph
    deductions_over_time = salary_records.values('month').annotate(total_deductions=Sum('deductions')).order_by('month')
    plt.figure(figsize=(10, 5))
    plt.plot([d['month'] for d in deductions_over_time], [d['total_deductions'] for d in deductions_over_time])
    plt.title('Deductions Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Deductions')
    graph = io.BytesIO()
    plt.savefig(graph, format='png')
    graph.seek(0)
    graph_png = base64.b64encode(graph.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'reporting/view_report.html', {
        'report': report,
        'salary_records': salary_records,
        'chart': chart_png,
        'graph': graph_png,
        'employees': employees
    })


def export_report(request, pk, export_format):
    report = Report.objects.get(pk=pk)
    salary_records = SalaryRecord.objects.filter(month__range=[report.start_date, report.end_date])
    employees = report.employees.all()
    df = pd.DataFrame(list(salary_records.values()))

    if export_format == 'pdf':
        html_string = render_to_string('reporting/export_pdf.html',
                                       {'report': report, 'salary_records': salary_records, 'employees': employees})
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'
        return response
    elif export_format == 'excel':
        # Set a different temp directory
        temp_dir = 'C:\\Users\\SHAMIR~1\\AppData\\Local\\Temp\\my_temp_dir'
        os.makedirs(temp_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False, suffix='.xlsx') as tmp:
            try:
                with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                tmp.seek(0)
                response = HttpResponse(tmp.read(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename="report_{pk}.xlsx"'
            finally:
                tmp.close()
                os.remove(tmp.name)
                shutil.rmtree(temp_dir)  # Remove the temp directory if needed
            return response

    return HttpResponse(status=400)
