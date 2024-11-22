# Generated by Django 5.0.6 on 2024-07-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary_processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaryrecord',
            name='allowances',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='salaryrecord',
            name='deductions',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
