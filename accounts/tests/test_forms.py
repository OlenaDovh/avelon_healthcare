"""Модуль `accounts/tests/test_forms.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest

from accounts.forms import (
    LoginForm,
    ProfileUpdateForm,
    RegisterForm,
    SupportPatientUpdateForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)


def get_profile_update_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_profile_update_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "email": "new@email.com",
        "phone": "+380991111111",
        "first_name": "Іван",
        "last_name": "Петренко",
        "middle_name": "Іванович",
        "birth_date": "",
        "preferred_contact_channel": "",
    }
    data.update(overrides)
    return data


def get_register_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_register_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "username": "testuser",
        "email": "test@email.com",
        "phone": "+380991111115",
        "first_name": "Іван",
        "last_name": "Петренко",
        "middle_name": "",
        "password1": "StrongPass123",
        "password2": "StrongPass123",
    }
    data.update(overrides)
    return data


def get_login_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_login_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "login": "testuser",
        "password": "testpass123",
    }
    data.update(overrides)
    return data


def get_support_patient_update_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_support_patient_update_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "first_name": "Іван",
        "last_name": "Петренко",
        "middle_name": "",
        "phone": "+380991111120",
        "birth_date": "",
        "preferred_contact_channel": "",
        "discount": 10,
    }
    data.update(overrides)
    return data


def get_password_change_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_password_change_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "old_password": "OldPass123",
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def get_set_password_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_set_password_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def prepare_user_for_login(user: Any, password: Any="testpass123", email_verified: Any=True, pending_email: Any="") -> Any:
    """Виконує прикладну логіку функції `prepare_user_for_login` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        password: Значення типу `Any`, яке передається для виконання логіки функції.
        email_verified: Значення типу `Any`, яке передається для виконання логіки функції.
        pending_email: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    user.set_password(password)
    user.email_verified = email_verified
    user.pending_email = pending_email
    user.save()
    return user


def prepare_user_for_password_change(user: Any, password: Any="OldPass123") -> Any:
    """Виконує прикладну логіку функції `prepare_user_for_password_change` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        password: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    user.set_password(password)
    user.save()
    return user


@pytest.mark.django_db
def test_profile_update_form_valid(user: Any) -> None:
    """Виконує прикладну логіку функції `test_profile_update_form_valid` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = ProfileUpdateForm(instance=user, data=get_profile_update_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_email_already_exists(user: Any, user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_profile_update_email_already_exists` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    other = user_factory(email="test@email.com")

    form = ProfileUpdateForm(
        instance=user,
        data=get_profile_update_data(
            email=other.email,
            phone="+380991111112",
            middle_name="",
        ),
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_profile_update_pending_email_conflict(user: Any, user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_profile_update_pending_email_conflict` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    other = user_factory(pending_email="test@email.com")

    form = ProfileUpdateForm(
        instance=user,
        data=get_profile_update_data(
            email=other.pending_email,
            phone="+380991111113",
            middle_name="",
        ),
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_profile_update_phone_already_exists(user: Any, user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_profile_update_phone_already_exists` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    other = user_factory(phone="+380991111114")

    form = ProfileUpdateForm(
        instance=user,
        data=get_profile_update_data(
            phone=other.phone,
            middle_name="",
        ),
    )

    assert not form.is_valid()
    assert "phone" in form.errors


@pytest.mark.django_db
def test_register_form_valid() -> None:
    """Виконує прикладну логіку функції `test_register_form_valid` у відповідному модулі проєкту.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = RegisterForm(data=get_register_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_email_already_exists(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_register_form_email_already_exists` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user_factory(email="test@email.com")

    form = RegisterForm(
        data=get_register_data(
            username="testuser2",
            email="test@email.com",
            phone="+380991111116",
            first_name="",
            last_name="",
        )
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_register_form_pending_email_conflict(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_register_form_pending_email_conflict` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user_factory(pending_email="test@email.com")

    form = RegisterForm(
        data=get_register_data(
            username="testuser3",
            email="test@email.com",
            phone="+380991111117",
            first_name="",
            last_name="",
        )
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_register_form_phone_already_exists(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_register_form_phone_already_exists` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user_factory(phone="+380991111118")

    form = RegisterForm(
        data=get_register_data(
            username="testuser4",
            email="new@email.com",
            phone="+380991111118",
            first_name="",
            last_name="",
        )
    )

    assert not form.is_valid()
    assert "phone" in form.errors


@pytest.mark.django_db
def test_login_form_valid_with_username(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_valid_with_username` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_valid_with_email(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_valid_with_email` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.email))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_requires_verified_email(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_requires_verified_email` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user, email_verified=False, pending_email="")

    form = LoginForm(data=get_login_data(login=user.username))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_allows_login_when_pending_email_exists(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_allows_login_when_pending_email_exists` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user, email_verified=False, pending_email="new@email.com")

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_username(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_invalid_with_wrong_username` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login="wrong_username"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_password(user: Any) -> None:
    """Виконує прикладну логіку функції `test_login_form_invalid_with_wrong_password` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username, password="wrong_password"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_valid(user: Any) -> None:
    """Виконує прикладну логіку функції `test_support_patient_update_form_valid` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_phone_already_exists(user: Any, user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_support_patient_update_form_phone_already_exists` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    other = user_factory(phone="+380991111121")

    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(phone=other.phone),
    )

    assert not form.is_valid()
    assert "phone" in form.errors


@pytest.mark.django_db
def test_support_patient_update_form_discount_invalid(user: Any) -> None:
    """Виконує прикладну логіку функції `test_support_patient_update_form_discount_invalid` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(
            phone="+380991111122",
            discount=120,
        ),
    )

    assert not form.is_valid()
    assert "discount" in form.errors


@pytest.mark.django_db
def test_user_password_change_form_valid(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_password_change_form_valid` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_wrong_old_password(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_password_change_form_wrong_old_password` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(old_password="WrongPass"),
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_set_password_form_passwords_do_not_match(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_set_password_form_passwords_do_not_match` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = UserSetPasswordForm(
        user=user,
        data=get_set_password_data(new_password2="AnotherPass"),
    )

    assert not form.is_valid()


def test_user_password_reset_form_has_email_field_attrs() -> None:
    """Виконує прикладну логіку функції `test_user_password_reset_form_has_email_field_attrs` у відповідному модулі проєкту.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = UserPasswordResetForm()

    assert form.fields["email"].label == "Електронна пошта"
    assert form.fields["email"].widget.attrs["class"] == "form-control"
