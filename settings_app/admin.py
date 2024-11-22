# settings_app/admin.py

from django.contrib import admin
from .models import TaxRate, Allowance

admin.site.register(TaxRate)
admin.site.register(Allowance)
