import pytest


@pytest.mark.django_db
def test_user_factory_creates_user(user):
    assert user.id is not None
    assert user.email
    assert user.phone
    assert user.username


@pytest.mark.django_db
def test_user_full_name_property(user):
    expected = " ".join(filter(None, [user.last_name, user.first_name, user.middle_name]))
    assert user.full_name == expected


@pytest.mark.django_db
def test_user_str_returns_full_name(user):
    assert str(user) == user.full_name