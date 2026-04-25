"""Модуль core/admin.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.contrib import admin
from .models import ClinicInfo, ContactInfo, Promotion

@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    """Клас ClinicInfoAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('title',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Клас ContactInfoAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('address', 'work_schedule', 'phone_1', 'email')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """Клас PromotionAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('title', 'end_date', 'created_at')
    list_filter = ('end_date',)
    search_fields = ('title', 'description')
