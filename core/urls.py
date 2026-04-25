"""Модуль `core/urls.py` застосунку `core`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.urls import path

from core.views import about_view, contacts_view, home_view, promotions_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("contacts/", contacts_view, name="contacts"),
    path("promotions/", promotions_view, name="promotions"),
]
