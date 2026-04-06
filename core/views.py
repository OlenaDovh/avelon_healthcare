from __future__ import annotations

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from doctors.models import Doctor
from analysis.models import Analysis

from .models import ClinicInfo, ContactInfo, Promotion

logger = logging.getLogger(__name__)


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає головну сторінку сайту.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь із головною сторінкою.
    """
    doctors = Doctor.objects.all()[:4]
    analyses = Analysis.objects.filter(is_active=True)[:3]
    promotions = Promotion.objects.all()[:3]

    logger.info("Відкрито головну сторінку.")

    return render(
        request,
        "avelon_healthcare/core/home.html",
        {
            "doctors": doctors,
            "analyses": analyses,
            "promotions": promotions,
        },
    )


def about_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку "Про клініку".

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою про клініку.
    """
    clinic_info = ClinicInfo.objects.first()

    logger.info("Відкрито сторінку 'Про клініку'.")

    return render(
        request,
        "avelon_healthcare/core/about.html",
        {"clinic_info": clinic_info},
    )


def contacts_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку контактів.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою контактів.
    """
    contacts = ContactInfo.objects.first()

    logger.info("Відкрито сторінку контактів.")

    return render(
        request,
        "avelon_healthcare/core/contacts.html",
        {"contacts": contacts},
    )


def promotions_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список акцій клініки.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою акцій.
    """
    promotions = Promotion.objects.all()

    logger.info("Відкрито сторінку акцій.")

    return render(
        request,
        "avelon_healthcare/core/promotions.html",
        {"promotions": promotions},
    )