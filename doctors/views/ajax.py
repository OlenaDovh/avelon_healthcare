from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from accounts.permissions import head_manager_required
from doctors.models import Direction


@login_required
@head_manager_required
def head_manager_load_doctor_directions_view(request: HttpRequest) -> JsonResponse:
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