"""Модуль reviews/admin.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Клас ReviewAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('user', 'appointment', 'created_at')
    search_fields = ('user__username', 'user__email', 'text', 'clinic_reply')
    readonly_fields = ('created_at',)
    fields = ('user', 'appointment', 'text', 'clinic_reply', 'created_at')
