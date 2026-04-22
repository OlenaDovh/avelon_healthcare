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


def get_profile_update_data(**overrides):
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


def get_register_data(**overrides):
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


def get_login_data(**overrides):
    data = {
        "login": "testuser",
        "password": "testpass123",
    }
    data.update(overrides)
    return data


def get_support_patient_update_data(**overrides):
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


def get_password_change_data(**overrides):
    data = {
        "old_password": "OldPass123",
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def get_set_password_data(**overrides):
    data = {
        "new_password1": "NewPass123",
        "new_password2": "NewPass123",
    }
    data.update(overrides)
    return data


def prepare_user_for_login(user, password="testpass123", email_verified=True, pending_email=""):
    user.set_password(password)
    user.email_verified = email_verified
    user.pending_email = pending_email
    user.save()
    return user


def prepare_user_for_password_change(user, password="OldPass123"):
    user.set_password(password)
    user.save()
    return user


@pytest.mark.django_db
def test_profile_update_form_valid(user):
    form = ProfileUpdateForm(instance=user, data=get_profile_update_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_email_already_exists(user, user_factory):
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
def test_profile_update_pending_email_conflict(user, user_factory):
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
def test_profile_update_phone_already_exists(user, user_factory):
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
def test_register_form_valid():
    form = RegisterForm(data=get_register_data())
    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_email_already_exists(user_factory):
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
def test_register_form_pending_email_conflict(user_factory):
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
def test_register_form_phone_already_exists(user_factory):
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
def test_login_form_valid_with_username(user):
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_valid_with_email(user):
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.email))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_requires_verified_email(user):
    prepare_user_for_login(user, email_verified=False, pending_email="")

    form = LoginForm(data=get_login_data(login=user.username))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_allows_login_when_pending_email_exists(user):
    prepare_user_for_login(user, email_verified=False, pending_email="new@email.com")

    form = LoginForm(data=get_login_data(login=user.username))
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_username(user):
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login="wrong_username"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_with_wrong_password(user):
    prepare_user_for_login(user)

    form = LoginForm(data=get_login_data(login=user.username, password="wrong_password"))
    assert not form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_valid(user):
    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_support_patient_update_form_phone_already_exists(user, user_factory):
    other = user_factory(phone="+380991111121")

    form = SupportPatientUpdateForm(
        instance=user,
        data=get_support_patient_update_data(phone=other.phone),
    )

    assert not form.is_valid()
    assert "phone" in form.errors


@pytest.mark.django_db
def test_support_patient_update_form_discount_invalid(user):
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
def test_user_password_change_form_valid(user):
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(),
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_wrong_old_password(user):
    prepare_user_for_password_change(user)

    form = UserPasswordChangeForm(
        user=user,
        data=get_password_change_data(old_password="WrongPass"),
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_set_password_form_passwords_do_not_match(user):
    form = UserSetPasswordForm(
        user=user,
        data=get_set_password_data(new_password2="AnotherPass"),
    )

    assert not form.is_valid()


def test_user_password_reset_form_has_email_field_attrs():
    form = UserPasswordResetForm()

    assert form.fields["email"].label == "Електронна пошта"
    assert form.fields["email"].widget.attrs["class"] == "form-control"