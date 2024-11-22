from django import forms


class GenerateReportForm(forms.Form):
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
        ('custom', 'Custom'),
    ]

    report_type = forms.ChoiceField(choices=REPORT_TYPE_CHOICES)
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2031)))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2031)))
