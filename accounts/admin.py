from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Адмін-панель для кастомного користувача.

    Додає відображення додаткових полів:
    - телефон
    - знижка
    - статус підтвердження email
    """

    model: type[User] = User

    fieldsets = UserAdmin.fieldsets + (
        ('Додаткові поля', {
            'fields': (
                'phone',
                'email_verified',
                'discount',
                'birth_date',
                'preferred_contact_channel',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додаткові поля', {
            'fields': ('email', 'phone'),
        }),
    )

    list_display = (
        'username',
        'first_name',
        'last_name',
        'middle_name',
        'phone',
        'email',
        'is_staff',
    )

    search_fields = ('username', 'email', 'phone')
