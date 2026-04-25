"""Модуль `doctors/views/__init__.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .ajax import head_manager_load_doctor_directions_view
from .head_manager import (
    head_manager_direction_create_view,
    head_manager_direction_list_view,
    head_manager_direction_update_view,
    head_manager_doctor_create_view,
    head_manager_doctor_list_view,
    head_manager_doctor_update_view,
    head_manager_schedule_create_view,
    head_manager_schedule_list_view,
    head_manager_schedule_update_view,
)
from .public import (
    direction_detail_view,
    direction_list_view,
    doctor_detail_view,
    doctor_list_view,
)
