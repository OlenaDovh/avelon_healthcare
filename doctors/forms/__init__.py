"""Модуль `doctors/forms/__init__.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .direction import DirectionForm
from .doctor import DoctorForm
from .schedule import DoctorWorkDayForm, DoctorWorkPeriodForm, DoctorWorkPeriodFormSet

__all__ = [
    "DirectionForm",
    "DoctorForm",
    "DoctorWorkDayForm",
    "DoctorWorkPeriodForm",
    "DoctorWorkPeriodFormSet",
]
