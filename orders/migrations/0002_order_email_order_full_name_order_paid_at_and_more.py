"""Модуль orders/migrations/0002_order_email_order_full_name_order_paid_at_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('orders', '0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.AddField(model_name='order', name='email', field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email')), migrations.AddField(model_name='order', name='full_name', field=models.CharField(blank=True, default='', max_length=255, verbose_name='ПІБ')), migrations.AddField(model_name='order', name='paid_at', field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплати')), migrations.AddField(model_name='order', name='payment_method', field=models.CharField(choices=[('online', 'Онлайн'), ('bank_transfer', 'На рахунок'), ('cash', 'На касі')], default='cash', max_length=30, verbose_name='Спосіб оплати')), migrations.AddField(model_name='order', name='phone', field=models.CharField(blank=True, default='', max_length=30, verbose_name='Телефон')), migrations.AlterField(model_name='order', name='status', field=models.CharField(choices=[('new', 'Нове'), ('paid', 'Сплачено'), ('completed', 'Завершено'), ('rejected', 'Відхилено')], default='new', max_length=20, verbose_name='Статус')), migrations.AlterField(model_name='order', name='user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'))]
