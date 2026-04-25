"""Модуль `orders/views/public.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import messages
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from analysis.models import Analysis
from orders.forms import AuthenticatedOrderForm, GuestOrderForm
from orders.services.checkout import create_order_from_analyses
from orders.services.forms import get_order_form
from orders.tasks import send_order_email_task


def _get_cart(request: HttpRequest) -> dict[str, int]:
    """Виконує прикладну логіку функції `_get_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        dict[str, int]: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return request.session.get("cart", {})


def _clear_cart(request: HttpRequest) -> None:
    """Виконує прикладну логіку функції `_clear_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request.session["cart"] = {}
    request.session.modified = True


@transaction.atomic
def order_create_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `order_create_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.method != "POST":
        messages.warning(request, "Некоректний спосіб запиту.")
        return redirect("analysis:cart_detail")

    cart = _get_cart(request)

    if not cart:
        messages.warning(request, "Кошик порожній.")
        return redirect("analysis:cart_detail")

    form: GuestOrderForm | AuthenticatedOrderForm = get_order_form(request)

    if not form.is_valid():
        messages.warning(request, "Перевірте правильність заповнення форми.")
        return redirect("analysis:cart_detail")

    analysis_ids = [int(item_id) for item_id in cart.keys()]
    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids, is_active=True)

    if not analyses.exists():
        messages.warning(request, "Не вдалося оформити замовлення.")
        return redirect("analysis:cart_detail")

    payment_method = form.cleaned_data["payment_method"]

    if request.user.is_authenticated:
        user = request.user

        last_name = user.last_name
        first_name = user.first_name
        middle_name = user.middle_name
        phone = getattr(user, "phone", "") or ""
        email = user.email or ""
    else:
        user = None

        last_name = form.cleaned_data["last_name"]
        first_name = form.cleaned_data["first_name"]
        middle_name = form.cleaned_data.get("middle_name", "")
        phone = form.cleaned_data["phone"]
        email = form.cleaned_data["email"]

    order = create_order_from_analyses(
        analyses=analyses,
        payment_method=payment_method,
        user=user,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        phone=phone,
        email=email,
    )

    transaction.on_commit(
        lambda: send_order_email_task.delay(order.id)
    )

    _clear_cart(request)

    messages.success(request, "Замовлення аналізів успішно оформлено.")

    if request.user.is_authenticated:
        return redirect("orders:order_detail", order_id=order.id)

    return redirect("core:home")
