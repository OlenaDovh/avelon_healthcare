"""Модуль doctors/migrations/0004_alter_doctor_options_alter_doctorworkday_options_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('doctors', '0003_doctor_user')]
    operations = [migrations.AlterModelOptions(name='doctor', options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Лікар', 'verbose_name_plural': 'Лікарі'}), migrations.AlterModelOptions(name='doctorworkday', options={'ordering': ['-work_date', 'doctor__last_name', 'doctor__first_name'], 'verbose_name': 'Розклад лікаря на дату', 'verbose_name_plural': 'Розклад лікарів на дати'}), migrations.RemoveField(model_name='doctor', name='full_name'), migrations.AddField(model_name='doctor', name='first_name', field=models.CharField(default='', max_length=150, verbose_name="Ім'я"), preserve_default=False), migrations.AddField(model_name='doctor', name='last_name', field=models.CharField(default='', max_length=150, verbose_name='Прізвище'), preserve_default=False), migrations.AddField(model_name='doctor', name='middle_name', field=models.CharField(blank=True, max_length=150, verbose_name='По батькові'))]
