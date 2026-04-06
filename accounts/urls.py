from __future__ import annotations

from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls import path, reverse_lazy

from .forms import UserSetPasswordForm
from .views import (
    UserPasswordResetView,
    login_view,
    logout_view,
    password_change_view,
    profile_update_view,
    profile_view,
    register_view,
)

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_update_view, name="profile_update"),
    path("password/change/", password_change_view, name="password_change"),

    path("password/reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name="avelon_healthcare/accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="avelon_healthcare/accounts/password_reset_confirm.html",
            form_class=UserSetPasswordForm,
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="avelon_healthcare/accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
