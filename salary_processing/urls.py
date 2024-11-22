# salary_processing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.calculate_salaries, name='calculate_salaries'),
    path('approve/<int:pk>/', views.approve_salaries, name='approve_salaries'),
    path('details/<int:pk>/', views.salary_details, name='salary_details'),
    path('disburse/<int:pk>/', views.disburse_salary, name='disburse_salary'),
]
