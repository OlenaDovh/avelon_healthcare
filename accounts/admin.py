from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Додаткові поля", {
            "fields": (
                "phone",
                "pending_email",
                "email_verified",
                "discount",
                "birth_date",
                "preferred_contact_channel",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Додаткові поля", {
            "fields": ("email", "phone"),
        }),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "middle_name",
        "phone",
        "email",
        "pending_email",
        "is_staff",
        "email_verified",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "email_verified",
    )

    search_fields = ("username", "email", "phone", "pending_email")

    def save_model(self, request, obj, form, change):
        if obj.email:
            obj.email_verified = True
            obj.pending_email = ""

        super().save_model(request, obj, form, change)