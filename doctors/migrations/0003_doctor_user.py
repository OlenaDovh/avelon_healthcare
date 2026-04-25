"""Модуль doctors/migrations/0003_doctor_user.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('doctors', '0002_doctorworkday_doctorworkperiod_and_more'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.AddField(model_name='doctor', name='user', field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_profile', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'))]
