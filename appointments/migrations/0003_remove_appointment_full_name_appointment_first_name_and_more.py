"""Модуль appointments/migrations/0003_remove_appointment_full_name_appointment_first_name_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.db import migrations, models

def fill_names(apps: Any, schema_editor: Any) -> None:
    """Виконує логіку `fill_names`.

Args:
    apps: Вхідне значення для виконання операції.
    schema_editor: Вхідне значення для виконання операції.

Returns:
    None."""
    Appointment = apps.get_model('appointments', 'Appointment')
    for obj in Appointment.objects.all():
        if not obj.first_name:
            obj.first_name = 'Невідомо'
        if not obj.last_name:
            obj.last_name = 'Невідомо'
        if obj.middle_name is None:
            obj.middle_name = ''
        obj.save(update_fields=['first_name', 'last_name', 'middle_name'])

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('appointments', '0002_appointment_email_appointment_full_name_and_more')]
    operations = [migrations.AddField(model_name='appointment', name='first_name', field=models.CharField(max_length=150, default='', verbose_name="Ім'я")), migrations.AddField(model_name='appointment', name='last_name', field=models.CharField(max_length=150, default='', verbose_name='Прізвище')), migrations.AddField(model_name='appointment', name='middle_name', field=models.CharField(max_length=150, blank=True, default='', verbose_name='По батькові')), migrations.RunPython(fill_names), migrations.AlterField(model_name='appointment', name='first_name', field=models.CharField(max_length=150, verbose_name="Ім'я")), migrations.AlterField(model_name='appointment', name='last_name', field=models.CharField(max_length=150, verbose_name='Прізвище'))]
