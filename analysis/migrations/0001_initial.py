"""Модуль analysis/migrations/0001_initial.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name='Analysis', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=255, verbose_name='Назва аналізу')), ('what_to_check', models.CharField(blank=True, max_length=255, verbose_name='Що перевірити')), ('disease', models.CharField(blank=True, max_length=255, verbose_name='Захворювання')), ('for_whom', models.CharField(blank=True, max_length=255, verbose_name='Для кого')), ('biomaterial', models.CharField(blank=True, max_length=255, verbose_name='Біоматеріал')), ('duration_days', models.PositiveIntegerField(verbose_name='Термін виконання (днів)')), ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')), ('is_active', models.BooleanField(default=True, verbose_name='Активний'))], options={'verbose_name': 'Аналіз', 'verbose_name_plural': 'Аналізи', 'ordering': ['name']})]
