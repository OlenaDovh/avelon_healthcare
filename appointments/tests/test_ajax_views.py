from typing import Any
import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_available_doctors_returns_doctors_for_direction(client: Any, direction: Any, doctor: Any) -> None:
    """Виконує логіку `test_available_doctors_returns_doctors_for_direction`.

Args:
    client: Вхідний параметр `client`.
    direction: Вхідний параметр `direction`.
    doctor: Вхідний параметр `doctor`.

Returns:
    Any: Результат виконання."""
    doctor.directions.add(direction)
    response = client.get(reverse('appointments:available_doctors'), {'direction_id': direction.id})
    assert response.status_code == 200
    data = response.json()
    assert any((item['id'] == doctor.id for item in data['doctors']))

@pytest.mark.django_db
def test_available_dates_returns_dates(client: Any, direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_available_dates_returns_dates`.

Args:
    client: Вхідний параметр `client`.
    direction: Вхідний параметр `direction`.
    doctor: Вхідний параметр `doctor`.
    monkeypatch: Вхідний параметр `monkeypatch`.

Returns:
    Any: Результат виконання."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.views.ajax.get_available_dates_for_doctor_direction', lambda doctor, direction, exclude_appointment_id=None: [target_date])
    response = client.get(reverse('appointments:available_dates'), {'doctor_id': doctor.id, 'direction_id': direction.id})
    assert response.status_code == 200
    assert response.json() == {'dates': [target_date]}

@pytest.mark.django_db
def test_available_slots_returns_slots(client: Any, direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_available_slots_returns_slots`.

Args:
    client: Вхідний параметр `client`.
    direction: Вхідний параметр `direction`.
    doctor: Вхідний параметр `doctor`.
    monkeypatch: Вхідний параметр `monkeypatch`.

Returns:
    Any: Результат виконання."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.views.ajax.get_available_slots_for_doctor_on_date', lambda doctor, direction, selected_date, exclude_appointment_id=None: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    response = client.get(reverse('appointments:available_slots'), {'doctor_id': doctor.id, 'direction_id': direction.id, 'date': target_date})
    assert response.status_code == 200
    assert response.json() == {'slots': [{'value': '10:00', 'label': '10:00 - 10:30'}]}
