"""Модуль orders/migrations/0004_remove_order_full_name_order_first_name_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('orders', '0003_order_rejection_reason')]
    operations = [migrations.RemoveField(model_name='order', name='full_name'), migrations.AddField(model_name='order', name='first_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name="Ім'я")), migrations.AddField(model_name='order', name='last_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name='Прізвище')), migrations.AddField(model_name='order', name='middle_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name='По батькові'))]
