# employee_portal/urls.py

from django.urls import path
from . import views
app_name = 'employee_portal'

urlpatterns = [
    path('', views.portal_home, name='portal_home'),
    path('generate_report/<str:report_type>/', views.generate_report, name='generate_report'),
]
