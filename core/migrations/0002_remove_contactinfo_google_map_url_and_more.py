"""Модуль core/migrations/0002_remove_contactinfo_google_map_url_and_more.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import migrations, models

class Migration(migrations.Migration):
    """Клас Migration.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RemoveField(model_name='contactinfo', name='google_map_url'), migrations.AddField(model_name='contactinfo', name='google_map_embed_url', field=models.TextField(blank=True, verbose_name='Google Maps Embed URL'))]
