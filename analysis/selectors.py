from __future__ import annotations
from typing import Any
from django.db.models import QuerySet
from analysis.models import Analysis


def active_analyses_queryset() -> QuerySet[Analysis]:
    """
    Повертає queryset активних аналізів.

    Returns:
        QuerySet[Analysis]: Набір активних аналізів.
    """
    return Analysis.objects.filter(is_active=True)


def filtered_analyses_queryset(
        *,
        what_to_check: str = "",
        disease: str = "",
        for_whom: str = "",
        biomaterial: str = "",
) -> QuerySet[Analysis]:
    """
    Повертає queryset аналізів із застосованими фільтрами.

    Args:
        what_to_check: Фільтр за полем "що перевірити".
        disease: Фільтр за захворюванням.
        for_whom: Фільтр за категорією "для кого".
        biomaterial: Фільтр за біоматеріалом.

    Returns:
        QuerySet[Analysis]: Відфільтрований набір аналізів.
    """
    analyses = active_analyses_queryset()

    if what_to_check:
        analyses = analyses.filter(what_to_check__icontains=what_to_check)

    if disease:
        analyses = analyses.filter(disease__icontains=disease)

    if for_whom:
        analyses = analyses.filter(for_whom__icontains=for_whom)

    if biomaterial:
        analyses = analyses.filter(biomaterial__icontains=biomaterial)

    return analyses


def analysis_filter_values() -> dict[str, QuerySet[Analysis, Any]]:
    """
    Повертає унікальні значення для фільтрів аналізів.

    Returns:
        dict[str, QuerySet[Analysis, Any]]: Словник значень для побудови фільтрів.
    """
    return {
        "what_to_check_values": (
            Analysis.objects.exclude(what_to_check="")
            .values_list("what_to_check", flat=True)
            .distinct()
            .order_by("what_to_check")
        ),
        "disease_values": (
            Analysis.objects.exclude(disease="")
            .values_list("disease", flat=True)
            .distinct()
            .order_by("disease")
        ),
        "for_whom_values": (
            Analysis.objects.exclude(for_whom="")
            .values_list("for_whom", flat=True)
            .distinct()
            .order_by("for_whom")
        ),
        "biomaterial_values": (
            Analysis.objects.exclude(biomaterial="")
            .values_list("biomaterial", flat=True)
            .distinct()
            .order_by("biomaterial")
        ),
    }
