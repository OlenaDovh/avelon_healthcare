"""Модуль `accounts/views/support.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.constants import PATIENT_GROUP
from accounts.forms import SupportPatientUpdateForm
from accounts.permissions import support_required

User = get_user_model()


@login_required
@support_required
def support_patient_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `support_patient_list_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    patients = User.objects.filter(
        groups__name=PATIENT_GROUP,
    ).order_by("last_name", "first_name", "username").distinct()

    paginator = Paginator(patients, 20)
    page_number: str | None = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "avelon_healthcare/accounts/pages/support_patient_list.html",
        {"page_obj": page_obj},
    )


@login_required
@support_required
def support_patient_update_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """Виконує прикладну логіку функції `support_patient_update_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        user_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    patient = get_object_or_404(
        User.objects.filter(groups__name=PATIENT_GROUP).distinct(),
        id=user_id,
    )

    if request.method == "POST":
        form = SupportPatientUpdateForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "Дані пацієнта успішно оновлено.")
            return redirect("accounts:support_patient_list")
    else:
        form = SupportPatientUpdateForm(instance=patient)

    return render(
        request,
        "avelon_healthcare/accounts/pages/support_patient_update.html",
        {
            "form": form,
            "patient": patient,
        },
    )
