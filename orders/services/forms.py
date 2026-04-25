"""Модуль `orders/services/forms.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.http import HttpRequest

from orders.forms import AuthenticatedOrderForm, GuestOrderForm


def get_order_form(request: HttpRequest) -> GuestOrderForm | AuthenticatedOrderForm:
    """Виконує прикладну логіку функції `get_order_form` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        GuestOrderForm | AuthenticatedOrderForm: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.user.is_authenticated:
        return AuthenticatedOrderForm(request.POST or None)
    return GuestOrderForm(request.POST or None)
