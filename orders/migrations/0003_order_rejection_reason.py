"""Модуль orders/migrations/0003_order_rejection_reason.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('orders', '0002_order_email_order_full_name_order_paid_at_and_more')]
    operations = [migrations.AddField(model_name='order', name='rejection_reason', field=models.TextField(blank=True, verbose_name='Причина відхилення'))]
