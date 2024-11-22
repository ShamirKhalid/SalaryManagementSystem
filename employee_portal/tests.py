# employee_portal/tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from salary_processing.models import SalaryRecord

User = get_user_model()

@pytest.mark.django_db
def test_generate_report_view():
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = Client()
    client.login(username='testuser', password='testpassword')

    # Create some salary records for the user
    employee = user.employee_management_profile
    SalaryRecord.objects.create(employee=employee, month='2023-06', basic_salary=1000, allowances=200, deductions=100, net_salary=1100)

    url = reverse('generate_report')
    response = client.get(url)

    assert response.status_code == 200
    assert 'application/pdf' in response['Content-Type']
    assert 'attachment; filename="salary_report.pdf"' in response['Content-Disposition']
