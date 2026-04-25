"""Модуль `doctors/views/ajax.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from accounts.permissions import head_manager_required
from doctors.models import Direction


@login_required
@head_manager_required
def head_manager_load_doctor_directions_view(request: HttpRequest) -> JsonResponse:
    """Виконує прикладну логіку функції `head_manager_load_doctor_directions_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctor_id = request.GET.get("doctor_id")

    directions_data: list[dict[str, str | int]] = []

    if doctor_id:
        directions = Direction.objects.filter(
            doctors__id=doctor_id
        ).distinct().order_by("name")

        directions_data = [
            {
                "id": direction.id,
                "name": direction.name,
            }
            for direction in directions
        ]

    return JsonResponse({"directions": directions_data})
