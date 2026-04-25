"""Модуль analysis/views/head_manager.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.permissions import head_manager_required
from analysis.forms import AnalysisForm
from analysis.models import Analysis

@login_required
@head_manager_required
def head_manager_analysis_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `head_manager_analysis_list_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    analyses = Analysis.objects.all().order_by('name')
    return render(request, 'avelon_healthcare/analysis/pages/head_manager_analysis_list.html', {'analyses': analyses})

@login_required
@head_manager_required
def head_manager_analysis_create_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `head_manager_analysis_create_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аналіз успішно створено.')
            return redirect('analysis:head_manager_analysis_list')
    else:
        form = AnalysisForm()
    return render(request, 'avelon_healthcare/analysis/pages/head_manager_analysis_form.html', {'form': form})

@login_required
@head_manager_required
def head_manager_analysis_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Виконує логіку `head_manager_analysis_update_view`.

Args:
    request: Вхідне значення для виконання операції.
    pk: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    analysis = get_object_or_404(Analysis, pk=pk)
    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аналіз успішно оновлено.')
            return redirect('analysis:head_manager_analysis_list')
    else:
        form = AnalysisForm(instance=analysis)
    return render(request, 'avelon_healthcare/analysis/pages/head_manager_analysis_form.html', {'form': form, 'analysis': analysis})
