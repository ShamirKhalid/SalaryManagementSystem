# SalaryManagementSystem/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('employee_management/', include('employee_management.urls')),
    path('salary_processing/', include('salary_processing.urls')),
    path('reporting/', include('reporting.urls')),
    path('settings/', include('settings_app.urls')),
    path('security/', include('security_access_control.urls')),
    path('employee_portal/', include('employee_portal.urls', namespace='employee_portal')),
    path('employee_auth/', include('employee_auth.urls', namespace='employee_auth')),
    path('', index, name='index'),
]
