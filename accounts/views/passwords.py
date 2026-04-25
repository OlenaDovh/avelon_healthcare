from __future__ import annotations
import logging
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from accounts.forms import UserPasswordChangeForm, UserPasswordResetForm
logger = logging.getLogger(__name__)

class UserPasswordResetView(PasswordResetView):
    """Описує клас `UserPasswordResetView`."""
    form_class = UserPasswordResetForm
    template_name = 'avelon_healthcare/accounts/pages/password_reset_form.html'
    email_template_name = 'avelon_healthcare/accounts/emails/password_reset_email.txt'
    subject_template_name = 'avelon_healthcare/accounts/emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form: UserPasswordResetForm) -> HttpResponse:
        """Виконує логіку `form_valid`.

Args:
    form: Вхідний параметр `form`.

Returns:
    Any: Результат виконання."""
        logger.info('Запит на відновлення пароля для email=%s', form.cleaned_data.get('email'))
        return super().form_valid(form)

@login_required
def password_change_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `password_change_view`.

Args:
    request: Вхідний параметр `request`.

Returns:
    Any: Результат виконання."""
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            logger.info('Користувач змінив пароль: %s', request.user.username)
            messages.success(request, 'Пароль успішно змінено.')
            return redirect('accounts:profile')
        logger.warning('Неуспішна спроба зміни пароля. user=%s', request.user.username)
    else:
        form = UserPasswordChangeForm(user=request.user)
    return render(request, 'avelon_healthcare/accounts/pages/password_change.html', {'form': form})
