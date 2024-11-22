# SalaryManagement/dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('salary-summary/', views.salary_summary, name='salary_summary'),
    # Add URLs for other components as needed
]
