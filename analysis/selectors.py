"""Модуль analysis/selectors.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.db.models import QuerySet
from analysis.models import Analysis

def active_analyses_queryset() -> QuerySet[Analysis]:
    """Виконує логіку `active_analyses_queryset`.

Returns:
    Результат виконання операції."""
    return Analysis.objects.filter(is_active=True)

def filtered_analyses_queryset(*, what_to_check: str='', disease: str='', for_whom: str='', biomaterial: str='') -> QuerySet[Analysis]:
    """Виконує логіку `filtered_analyses_queryset`.

Args:
    what_to_check: Вхідне значення для виконання операції.
    disease: Вхідне значення для виконання операції.
    for_whom: Вхідне значення для виконання операції.
    biomaterial: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
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
    """Виконує логіку `analysis_filter_values`.

Returns:
    Результат виконання операції."""
    return {'what_to_check_values': Analysis.objects.exclude(what_to_check='').values_list('what_to_check', flat=True).distinct().order_by('what_to_check'), 'disease_values': Analysis.objects.exclude(disease='').values_list('disease', flat=True).distinct().order_by('disease'), 'for_whom_values': Analysis.objects.exclude(for_whom='').values_list('for_whom', flat=True).distinct().order_by('for_whom'), 'biomaterial_values': Analysis.objects.exclude(biomaterial='').values_list('biomaterial', flat=True).distinct().order_by('biomaterial')}
