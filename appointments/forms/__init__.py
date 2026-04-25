"""Модуль `appointments/forms/__init__.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .create import AppointmentCreateForm, GuestAppointmentCreateForm
from .support import SupportAppointmentCreateForm
from .update import SupportAppointmentUpdateForm

__all__ = [
    "AppointmentCreateForm",
    "GuestAppointmentCreateForm",
    "SupportAppointmentCreateForm",
    "SupportAppointmentUpdateForm",
]
