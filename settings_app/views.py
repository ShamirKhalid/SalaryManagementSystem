# settings_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import TaxRate, Allowance
from .forms import TaxRateForm, AllowanceForm

def settings(request):
    tax_rates = TaxRate.objects.all()
    allowances = Allowance.objects.all()
    return render(request, 'settings_app/settings.html', {'tax_rates': tax_rates, 'allowances': allowances})

def add_tax_rate(request):
    if request.method == 'POST':
        form = TaxRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = TaxRateForm()
    return render(request, 'settings_app/tax_rates.html', {'form': form})

def add_allowance(request):
    if request.method == 'POST':
        form = AllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = AllowanceForm()
    return render(request, 'settings_app/allowances.html', {'form': form})

def edit_tax_rate(request, pk):
    tax_rate = get_object_or_404(TaxRate, pk=pk)
    if request.method == 'POST':
        form = TaxRateForm(request.POST, instance=tax_rate)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = TaxRateForm(instance=tax_rate)
    return render(request, 'settings_app/tax_rates.html', {'form': form})

def edit_allowance(request, pk):
    allowance = get_object_or_404(Allowance, pk=pk)
    if request.method == 'POST':
        form = AllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = AllowanceForm(instance=allowance)
    return render(request, 'settings_app/allowances.html', {'form': form})

def delete_tax_rate(request, pk):
    tax_rate = get_object_or_404(TaxRate, pk=pk)
    if request.method == 'POST':
        tax_rate.delete()
        return redirect('settings')
    return render(request, 'settings_app/delete_confirm.html', {'object': tax_rate})

def delete_allowance(request, pk):
    allowance = get_object_or_404(Allowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('settings')
    return render(request, 'settings_app/delete_confirm.html', {'object': allowance})

def tax_rates_view(request):
    tax_rates_list = TaxRate.objects.all()
    return render(request, 'settings_app/tax_rates.html', {'tax_rates': tax_rates_list})

def allowances_view(request):
    allowances_list = Allowance.objects.all()
    return render(request, 'settings_app/allowances.html', {'allowances': allowances_list})
