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


def get_profile_update_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для оновлення профілю.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми оновлення профілю.
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


def get_register_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для реєстрації користувача.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми реєстрації.
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


def get_login_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для входу користувача.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми входу.
    """
    data = {
        "login": "testuser",
        "password": "testpass123",
    }
    data.update(overrides)
    return data


def get_support_patient_update_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для оновлення пацієнта support-користувачем.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми оновлення пацієнта.
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


def get_password_change_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для зміни пароля.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми зміни пароля.
    """
    data = {
        "old_password": "OldPass123",
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def get_set_password_data(**overrides: object) -> dict[str, object]:
    """
    Формує тестові дані для встановлення нового пароля.

    Args:
        **overrides: Значення для перевизначення стандартних даних.

    Returns:
        dict[str, object]: Дані форми встановлення пароля.
    """
    data = {
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def prepare_user_for_login(
    user: object,
    password: str = "testpass123",
    email_verified: bool = True,
    pending_email: str = "",
) -> object:
    """
    Готує користувача до тестування форми входу.

    Args:
        user: Об'єкт користувача.
        password: Пароль користувача.
        email_verified: Ознака підтвердження email.
        pending_email: Email, що очікує підтвердження.

    Returns:
        object: Оновлений користувач.
    """
    user.set_password(password)
    user.email_verified = email_verified
    user.pending_email = pending_email
    user.save()
    return user


def prepare_user_for_password_change(
    user: object,
    password: str = "OldPass123",
) -> object:
    """
    Готує користувача до тестування зміни пароля.

    Args:
        user: Об'єкт користувача.
        password: Поточний пароль користувача.

    Returns:
        object: Оновлений користувач.
    """
    user.set_password(password)
    user.save()
    return user


@pytest.mark.django_db
def test_profile_update_form_valid(user: object) -> None:
    """
    Перевіряє валідність форми оновлення профілю.

    Args:
        user: Тестовий користувач.
    """
    form = ProfileUpdateForm(instance=user, data=get_profile_update_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_email_already_exists(
    user: object,
    user_factory: object,
) -> None:
    """
    Перевіряє помилку, якщо email вже використовується.

    Args:
        user: Тестовий користувач.
        user_factory: Фабрика для створення користувачів.
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
def test_profile_update_pending_email_conflict(
    user: object,
    user_factory: object,
) -> None:
    """
    Перевіряє помилку, якщо email очікує підтвердження в іншого користувача.

    Args:
        user: Тестовий користувач.
        user_factory: Фабрика для створення користувачів.
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
def test_profile_update_phone_already_exists(
    user: object,
    user_factory: object,
) -> None:
    """
    Перевіряє помилку, якщо телефон вже використовується.

    Args:
        user: Тестовий користувач.
        user_factory: Фабрика для створення користувачів.
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
    """
    Перевіряє валідність форми реєстрації.
    """
    form = RegisterForm(data=get_register_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_email_already_exists(user_factory: object) -> None:
    """
    Перевіряє помилку реєстрації, якщо email вже використовується.

    Args:
        user_factory: Фабрика для створення користувачів.
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
def test_register_form_pending_email_conflict(user_factory: object) -> None:
    """
    Перевіряє помилку реєстрації, якщо email очікує підтвердження.

    Args:
        user_factory: Фабрика для створення користувачів.
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
def test_register_form_phone_already_exists(user_factory: object) -> None:
    """
    Перевіряє помилку реєстрації, якщо телефон вже використовується.

    Args:
        user_factory: Фабрика для створення користувачів.
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
def test_login_form_valid_with_username(user: object) -> None:
    """
    Перевіряє валідність форми входу за username.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_valid_with_email(user: object) -> None:
    """
    Перевіряє валідність форми входу за email.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.email))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_requires_verified_email(user: object) -> None:
    """
    Перевіряє заборону входу без підтвердженого email.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user, email_verified=False, pending_email="")

    form = LoginForm(data=get_login_data(login=user.username))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_allows_login_when_pending_email_exists(user: object) -> None:
    """
    Перевіряє дозвіл входу, якщо є pending_email.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user, email_verified=False, pending_email="new@email.com")

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_username(user: object) -> None:
    """
    Перевіряє помилку входу з неправильним username.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login="wrong_username"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_password(user: object) -> None:
    """
    Перевіряє помилку входу з неправильним паролем.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username, password="wrong_password"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_valid(user: object) -> None:
    """
    Перевіряє валідність форми оновлення пацієнта support-користувачем.

    Args:
        user: Тестовий користувач.
    """
    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_phone_already_exists(
    user: object,
    user_factory: object,
) -> None:
    """
    Перевіряє помилку, якщо телефон пацієнта вже використовується.

    Args:
        user: Тестовий користувач.
        user_factory: Фабрика для створення користувачів.
    """
    other = user_factory(phone="+380991111121")

    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(phone=other.phone),
    )

    assert not form.is_valid()
    assert "phone" in form.errors


@pytest.mark.django_db
def test_support_patient_update_form_discount_invalid(user: object) -> None:
    """
    Перевіряє помилку, якщо знижка має некоректне значення.

    Args:
        user: Тестовий користувач.
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
def test_user_password_change_form_valid(user: object) -> None:
    """
    Перевіряє валідність форми зміни пароля.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_wrong_old_password(user: object) -> None:
    """
    Перевіряє помилку при неправильному старому паролі.

    Args:
        user: Тестовий користувач.
    """
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(old_password="WrongPass"),
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_set_password_form_passwords_do_not_match(user: object) -> None:
    """
    Перевіряє помилку, якщо нові паролі не збігаються.

    Args:
        user: Тестовий користувач.
    """
    form = UserSetPasswordForm(
        user=user,
        data=get_set_password_data(new_password2="AnotherPass"),
    )

    assert not form.is_valid()


def test_user_password_reset_form_has_email_field_attrs() -> None:
    """
    Перевіряє налаштування поля email у формі скидання пароля.
    """
    form = UserPasswordResetForm()

    assert form.fields["email"].label == "Електронна пошта"
    assert form.fields["email"].widget.attrs["class"] == "form-control"