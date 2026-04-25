"""Модуль appointments/migrations/0004_remove_appointment_full_name_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('appointments', '0003_remove_appointment_full_name_appointment_first_name_and_more')]
    operations = [migrations.RemoveField(model_name='appointment', name='full_name'), migrations.AlterField(model_name='appointment', name='first_name', field=models.CharField(max_length=150, verbose_name='Імʼя')), migrations.AlterField(model_name='appointment', name='middle_name', field=models.CharField(blank=True, max_length=150, verbose_name='По батькові'))]
