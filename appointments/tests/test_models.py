import pytest
from django.core.exceptions import ValidationError

from appointments.models import AppointmentStatus


@pytest.mark.django_db
def test_appointment_factory_creates_appointment(appointment):
    assert appointment.id is not None
    assert appointment.status == AppointmentStatus.PLANNED


@pytest.mark.django_db
def test_appointment_full_name_property(appointment):
    expected = " ".join(
        filter(None, [appointment.last_name, appointment.first_name, appointment.middle_name])
    )
    assert appointment.full_name == expected


@pytest.mark.django_db
def test_appointment_customer_name_returns_full_name(appointment):
    assert appointment.customer_name == appointment.full_name


@pytest.mark.django_db
def test_appointment_clean_raises_if_doctor_not_in_direction(appointment, direction_factory):
    appointment.direction = direction_factory()

    with pytest.raises(ValidationError):
        appointment.clean()


@pytest.mark.django_db
def test_appointment_clean_requires_rejection_reason(appointment):
    appointment.status = AppointmentStatus.REJECTED
    appointment.rejection_reason = ""

    with pytest.raises(ValidationError):
        appointment.clean()