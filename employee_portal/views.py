# employee_portal/views.py
import io
from django.contrib.auth import logout
import pdfkit
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from salary_processing.models import SalaryRecord


@login_required
def portal_home(request):
    employee = request.user.employee_management_profile
    salary_records = SalaryRecord.objects.filter(employee=employee)
    return render(request, 'employee_portal/portal_home.html', {'salary_records': salary_records})


@login_required
def generate_report(request, report_type):
    employee = request.user.employee_management_profile
    salary_records = SalaryRecord.objects.filter(employee=employee)

    context = {
        'employee': employee,
        'salary_records': salary_records,
        'report_type': report_type,
    }

    if report_type == 'pdf':
        html = render_to_string('employee_portal/report_template.html', context)
        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="salary_report.pdf"'
        return response
    elif report_type == 'excel':
        # Code to generate Excel report
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Add headers
        headers = ['Month', 'Basic Salary', 'Allowances', 'Deductions', 'Net Salary', 'Approved']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Add data
        for row_num, record in enumerate(salary_records, 1):
            worksheet.write(row_num, 0, record.month.strftime('%B %Y'))
            worksheet.write(row_num, 1, record.basic_salary)
            worksheet.write(row_num, 2, record.allowances)
            worksheet.write(row_num, 3, record.deductions)
            worksheet.write(row_num, 4, record.net_salary)
            worksheet.write(row_num, 5, 'Yes' if record.is_approved else 'No')

        workbook.close()
        output.seek(0)

        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="salary_report.xlsx"'
        return response

    return redirect('portal_home')


def employee_logout(request):
    logout(request)
    return redirect('employee_auth:employee_login')
