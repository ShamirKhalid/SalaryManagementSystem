from django import forms
from .models import SalaryRecord
import datetime

class MonthYearWidget(forms.DateInput):
    input_type = 'month'
    format = '%Y-%m'

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-control'}
        super().__init__(attrs=attrs, format=self.format)

    def format_value(self, value):
        if value is not None and isinstance(value, (datetime.date, datetime.datetime)):
            return value.strftime(self.format)
        return value

class CalculateSalaryForm(forms.ModelForm):
    month = forms.DateField(widget=MonthYearWidget(), input_formats=['%Y-%m'])

    class Meta:
        model = SalaryRecord
        fields = ['employee', 'month']

class ApproveSalaryForm(forms.ModelForm):
    class Meta:
        model = SalaryRecord
        fields = ['is_approved']

class DisburseSalaryForm(forms.ModelForm):
    class Meta:
        model = SalaryRecord
        fields = []
