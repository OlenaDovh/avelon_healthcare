"""Модуль `appointments/services/__init__.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .availability import (
    get_available_dates_for_doctor_direction,
    get_available_slots_for_doctor_on_date,
)
from .creation import (
    fill_appointment_from_guest_data,
    fill_appointment_from_user,
    save_new_appointment,
)
from .notifications import send_appointment_email
