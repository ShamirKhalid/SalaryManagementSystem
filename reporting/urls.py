# reporting/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_report, name='generate_report'),
    path('list/', views.report_list, name='report_list'),
    path('view/<int:pk>/', views.view_report, name='view_report'),
    path('export/<int:pk>/<str:export_format>/', views.export_report, name='export_report'),  # Use 'export_format'
]
