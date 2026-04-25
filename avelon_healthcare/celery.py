"""Модуль `avelon_healthcare/celery.py` застосунку `avelon_healthcare`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avelon_healthcare.settings.local")

app = Celery("avelon_healthcare")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
