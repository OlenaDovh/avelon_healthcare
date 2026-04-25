"""Модуль accounts/migrations/0004_alter_user_discount.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('accounts', '0003_user_pending_email')]
    operations = [migrations.AlterField(model_name='user', name='discount', field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Знижка, %'))]
