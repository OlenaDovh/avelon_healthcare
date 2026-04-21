from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpRequest

UserModel = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> UserModel | None:
        login_value: str | None = username or kwargs.get("email")

        if not login_value or not password:
            return None

        user = UserModel.objects.filter(
            Q(username__iexact=login_value) | Q(email__iexact=login_value)
        ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None