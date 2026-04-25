"""Модуль accounts/migrations/0002_user_middle_name_alter_user_first_name_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('accounts', '0001_initial')]
    operations = [migrations.AddField(model_name='user', name='middle_name', field=models.CharField(blank=True, max_length=150, verbose_name='По батькові')), migrations.AlterField(model_name='user', name='first_name', field=models.CharField(max_length=150, verbose_name="Ім'я")), migrations.AlterField(model_name='user', name='is_staff', field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')), migrations.AlterField(model_name='user', name='last_name', field=models.CharField(max_length=150, verbose_name='Прізвище'))]
