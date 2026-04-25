"""Модуль appointments/migrations/0002_appointment_email_appointment_full_name_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('appointments', '0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.AddField(model_name='appointment', name='email', field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email')), migrations.AddField(model_name='appointment', name='full_name', field=models.CharField(blank=True, default='', max_length=255, verbose_name='ПІБ')), migrations.AddField(model_name='appointment', name='phone', field=models.CharField(blank=True, default='', max_length=30, verbose_name='Телефон')), migrations.AlterField(model_name='appointment', name='user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'))]
