"""Модуль analysis/admin.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.contrib import admin
from .models import Analysis

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    """Клас AnalysisAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('name', 'what_to_check', 'disease', 'for_whom', 'biomaterial', 'duration_days', 'price', 'is_active')
    list_filter = ('what_to_check', 'disease', 'for_whom', 'biomaterial', 'is_active')
    search_fields = ('name', 'what_to_check', 'disease', 'for_whom', 'biomaterial')
