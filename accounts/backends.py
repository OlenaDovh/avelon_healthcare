from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpRequest

UserModel = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Backend автентифікації користувача за логіном або email.

    Дозволяє користувачу входити в систему, використовуючи
    або значення поля username, або значення поля email.
    """

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> UserModel | None:
        """
        Автентифікує користувача за логіном або email і паролем.

        Args:
            request (HttpRequest | None): Об'єкт HTTP-запиту.
            username (str | None): Логін або email користувача.
            password (str | None): Пароль користувача.
            **kwargs (Any): Додаткові параметри.

        Returns:
            User | None: Об'єкт користувача у разі успішної
            автентифікації, інакше None.
        """
        login_value: str | None = username or kwargs.get("email")

        if not login_value or not password:
            return None

        try:
            user = UserModel.objects.get(
                Q(username__iexact=login_value) | Q(email__iexact=login_value)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None