"""Модуль `appointments/migrations/0003_remove_appointment_full_name_appointment_first_name_and_more.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
from django.db import migrations, models


def fill_names(apps: Any, schema_editor: Any) -> None:
    """Виконує прикладну логіку функції `fill_names` у відповідному модулі проєкту.

    Параметри:
        apps: Значення типу `Any`, яке передається для виконання логіки функції.
        schema_editor: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    Appointment = apps.get_model("appointments", "Appointment")

    for obj in Appointment.objects.all():
        if not obj.first_name:
            obj.first_name = "Невідомо"
        if not obj.last_name:
            obj.last_name = "Невідомо"
        if obj.middle_name is None:
            obj.middle_name = ""

        obj.save(update_fields=["first_name", "last_name", "middle_name"])


class Migration(migrations.Migration):

    """Клас `Migration` інкапсулює повʼязану логіку проєкту.

    Базові класи: `migrations.Migration`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    dependencies = [
        ("appointments", "0002_appointment_email_appointment_full_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="first_name",
            field=models.CharField(max_length=150, default="", verbose_name="Ім'я"),
        ),
        migrations.AddField(
            model_name="appointment",
            name="last_name",
            field=models.CharField(max_length=150, default="", verbose_name="Прізвище"),
        ),
        migrations.AddField(
            model_name="appointment",
            name="middle_name",
            field=models.CharField(max_length=150, blank=True, default="", verbose_name="По батькові"),
        ),

        migrations.RunPython(fill_names),

        migrations.AlterField(
            model_name="appointment",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="Ім'я"),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="Прізвище"),
        ),
    ]
