"""Модуль `core/views/pages.py` застосунку `core`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from analysis.models import Analysis
from core.models import ClinicInfo, ContactInfo, Promotion
from daily_horoscope.services import get_or_create_daily_horoscope_for_session
from doctors.models import Doctor


def home_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `home_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctors = Doctor.objects.all()[:4]
    analyses = Analysis.objects.filter(is_active=True)[:3]
    promotions = Promotion.objects.all()[:3]
    horoscope_data = get_or_create_daily_horoscope_for_session(request)

    return render(
        request,
        "avelon_healthcare/core/pages/home.html",
        {
            "doctors": doctors,
            "analyses": analyses,
            "promotions": promotions,
            "horoscope_text": horoscope_data["text"],
            "horoscope_theme": horoscope_data.get("theme"),
        },
    )


def about_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `about_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    clinic_info = ClinicInfo.objects.first()
    return render(
        request,
        "avelon_healthcare/core/pages/about.html",
        {"clinic_info": clinic_info},
    )


def contacts_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `contacts_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    contacts = ContactInfo.objects.first()
    return render(
        request,
        "avelon_healthcare/core/pages/contacts.html",
        {"contacts": contacts},
    )


def promotions_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `promotions_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    promotions = Promotion.objects.all()
    return render(
        request,
        "avelon_healthcare/core/pages/promotions.html",
        {"promotions": promotions},
    )
