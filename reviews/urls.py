"""Модуль `reviews/urls.py` застосунку `reviews`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.urls import path

from .views import review_create_view, review_list_view, support_review_reply_view, support_review_list_view

app_name = "reviews"

urlpatterns = [
    path("", review_list_view, name="review_list"),
    path("create/<int:appointment_id>/", review_create_view, name="review_create"),
    path("staff/", support_review_list_view, name="support_review_list"),
    path("staff/<int:review_id>/reply/", support_review_reply_view, name="support_review_reply"),
]
