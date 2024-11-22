# employee_auth/urls.py

from django.urls import path
from . import views

app_name = 'employee_auth'  # Add this line

urlpatterns = [
    path('register/', views.employee_register, name='employee_register'),
    path('login/', views.employee_login, name='employee_login'),
    path('logout/', views.employee_logout, name='employee_logout'),
    path('password_reset/', views.employee_password_reset, name='employee_password_reset'),
    path('password_reset_done/', views.employee_password_reset_done, name='employee_password_reset_done'),
    path('reset/<uidb64>/<token>/', views.employee_password_reset_confirm, name='employee_password_reset_confirm'),
    path('reset/done/', views.employee_password_reset_complete, name='employee_password_reset_complete'),
]
