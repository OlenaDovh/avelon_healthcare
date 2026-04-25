from typing import Any
import pytest
from analysis.selectors import active_analyses_queryset, analysis_filter_values, filtered_analyses_queryset

@pytest.mark.django_db
def test_active_analyses_queryset_returns_only_active(analysis_factory: Any) -> None:
    """Виконує логіку `test_active_analyses_queryset_returns_only_active`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    active_analysis = analysis_factory(is_active=True)
    inactive_analysis = analysis_factory(is_active=False)
    result = active_analyses_queryset()
    assert active_analysis in result
    assert inactive_analysis not in result

@pytest.mark.django_db
def test_filtered_analyses_queryset_filters_by_what_to_check(analysis_factory: Any) -> None:
    """Виконує логіку `test_filtered_analyses_queryset_filters_by_what_to_check`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    matched = analysis_factory(what_to_check='Гемоглобін', is_active=True)
    analysis_factory(what_to_check='Глюкоза', is_active=True)
    result = filtered_analyses_queryset(what_to_check='гемо')
    assert matched in result
    assert result.count() == 1

@pytest.mark.django_db
def test_filtered_analyses_queryset_filters_by_disease(analysis_factory: Any) -> None:
    """Виконує логіку `test_filtered_analyses_queryset_filters_by_disease`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    matched = analysis_factory(disease='Анемія', is_active=True)
    analysis_factory(disease='Діабет', is_active=True)
    result = filtered_analyses_queryset(disease='анем')
    assert matched in result
    assert result.count() == 1

@pytest.mark.django_db
def test_filtered_analyses_queryset_filters_by_for_whom(analysis_factory: Any) -> None:
    """Виконує логіку `test_filtered_analyses_queryset_filters_by_for_whom`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    matched = analysis_factory(for_whom='Для дітей', is_active=True)
    analysis_factory(for_whom='Для дорослих', is_active=True)
    result = filtered_analyses_queryset(for_whom='діт')
    assert matched in result
    assert result.count() == 1

@pytest.mark.django_db
def test_filtered_analyses_queryset_filters_by_biomaterial(analysis_factory: Any) -> None:
    """Виконує логіку `test_filtered_analyses_queryset_filters_by_biomaterial`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    matched = analysis_factory(biomaterial='Кров', is_active=True)
    analysis_factory(biomaterial='Сеча', is_active=True)
    result = filtered_analyses_queryset(biomaterial='кро')
    assert matched in result
    assert result.count() == 1

@pytest.mark.django_db
def test_analysis_filter_values_returns_distinct_values(analysis_factory: Any) -> None:
    """Виконує логіку `test_analysis_filter_values_returns_distinct_values`.

Args:
    analysis_factory: Вхідний параметр `analysis_factory`.

Returns:
    Any: Результат виконання."""
    analysis_factory(what_to_check='Гемоглобін', disease='Анемія', for_whom='Для дорослих', biomaterial='Кров')
    analysis_factory(what_to_check='Гемоглобін', disease='Анемія', for_whom='Для дорослих', biomaterial='Кров')
    analysis_factory(what_to_check='Глюкоза', disease='Діабет', for_whom='Для дітей', biomaterial='Сеча')
    result = analysis_filter_values()
    assert 'Гемоглобін' in list(result['what_to_check_values'])
    assert 'Анемія' in list(result['disease_values'])
    assert 'Для дорослих' in list(result['for_whom_values'])
    assert 'Кров' in list(result['biomaterial_values'])
