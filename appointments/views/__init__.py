"""Модуль `appointments/views/__init__.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .ajax import available_dates, available_doctors, available_slots
from .patient import (
    appointment_cancel_view,
    appointment_detail_view,
    appointment_list_view,
)
from .public import appointment_create_view
from .support import (
    support_appointment_create_view,
    support_appointment_list_view,
    support_appointment_update_view,
)
