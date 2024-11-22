# settings_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings, name='settings'),
    path('tax_rates/', views.tax_rates_view, name='tax_rates'),  # Updated to use tax_rates_view
    path('add_tax_rate/', views.add_tax_rate, name='add_tax_rate'),
    path('edit_tax_rate/<int:pk>/', views.edit_tax_rate, name='edit_tax_rate'),
    path('delete_tax_rate/<int:pk>/', views.delete_tax_rate, name='delete_tax_rate'),
    path('allowances/', views.allowances_view, name='allowances'),  # Updated to use allowances_view
    path('add_allowance/', views.add_allowance, name='add_allowance'),
    path('edit_allowance/<int:pk>/', views.edit_allowance, name='edit_allowance'),
    path('delete_allowance/<int:pk>/', views.delete_allowance, name='delete_allowance'),
]
