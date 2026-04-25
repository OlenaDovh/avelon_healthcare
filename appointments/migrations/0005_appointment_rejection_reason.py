"""Модуль appointments/migrations/0005_appointment_rejection_reason.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('appointments', '0004_remove_appointment_full_name_and_more')]
    operations = [migrations.AddField(model_name='appointment', name='rejection_reason', field=models.TextField(blank=True, verbose_name='Причина відхилення'))]
