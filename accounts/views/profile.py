"""Модуль accounts/views/profile.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from accounts.forms import ProfileUpdateForm
from accounts.permissions import is_staff_role
from accounts.services import send_verification_email
logger = logging.getLogger(__name__)

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `profile_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return render(request, 'avelon_healthcare/accounts/pages/profile.html')

@login_required
def profile_update_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `profile_update_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if request.method == 'POST':
        current_email: str = request.user.email
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            requested_email: str = form.cleaned_data['email']
            email_changed: bool = current_email.lower() != requested_email.lower()
            if email_changed:
                user.pending_email = requested_email
                user.email_verified = False
                user.email = current_email
            elif not user.pending_email:
                user.email_verified = True
            user.save()
            if email_changed:
                send_verification_email(request=request, user=user, target_email=user.pending_email, subject='Avelon Healthcare — підтвердження нової електронної пошти')
                logger.info('Користувач ініціював зміну email. user=%s pending_email=%s', request.user.username, user.pending_email)
                messages.warning(request, 'Ми надіслали лист для підтвердження нової електронної пошти. Поточна адреса залишиться активною, доки ви не підтвердите нову.')
            else:
                logger.info('Оновлено профіль користувача: %s', request.user.username)
                messages.success(request, 'Профіль успішно оновлено.')
            return redirect('accounts:profile')
        logger.warning('Неуспішна спроба оновлення профілю. user=%s', request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'avelon_healthcare/accounts/pages/profile_update.html', {'form': form})

@login_required
def staff_dashboard_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `staff_dashboard_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if not is_staff_role(request.user):
        return redirect('accounts:profile')
    return render(request, 'avelon_healthcare/accounts/pages/staff_dashboard.html')
