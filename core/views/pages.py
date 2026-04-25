"""Модуль core/views/pages.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from analysis.models import Analysis
from core.models import ClinicInfo, ContactInfo, Promotion
from daily_horoscope.services import get_or_create_daily_horoscope_for_session
from doctors.models import Doctor

def home_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `home_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    doctors = Doctor.objects.all()[:4]
    analyses = Analysis.objects.filter(is_active=True)[:3]
    promotions = Promotion.objects.all()[:3]
    horoscope_data = get_or_create_daily_horoscope_for_session(request)
    return render(request, 'avelon_healthcare/core/pages/home.html', {'doctors': doctors, 'analyses': analyses, 'promotions': promotions, 'horoscope_text': horoscope_data['text'], 'horoscope_theme': horoscope_data.get('theme')})

def about_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `about_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    clinic_info = ClinicInfo.objects.first()
    return render(request, 'avelon_healthcare/core/pages/about.html', {'clinic_info': clinic_info})

def contacts_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `contacts_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    contacts = ContactInfo.objects.first()
    return render(request, 'avelon_healthcare/core/pages/contacts.html', {'contacts': contacts})

def promotions_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `promotions_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    promotions = Promotion.objects.all()
    return render(request, 'avelon_healthcare/core/pages/promotions.html', {'promotions': promotions})
