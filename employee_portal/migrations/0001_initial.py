# Generated by Django 5.0.6 on 2024-07-20 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee_management', '0002_employee_bank_account_number_employee_bank_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField()),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
            ],
        ),
    ]
