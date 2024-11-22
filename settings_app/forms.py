# settings_app/forms.py

from django import forms
from .models import TaxRate, Allowance

class TaxRateForm(forms.ModelForm):
    class Meta:
        model = TaxRate
        fields = ['name', 'rate']

class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = ['name', 'amount']
