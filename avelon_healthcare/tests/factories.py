from typing import Any
import factory
from decimal import Decimal
from datetime import date, time, timedelta
from django.contrib.auth import get_user_model
from analysis.models import Analysis
from appointments.models import Appointment, AppointmentStatus
from core.models import ClinicInfo, ContactInfo, Promotion
from doctors.models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod
from orders.models import Order, OrderItem, OrderStatus, PaymentMethod
from reviews.models import Review
from support_chat.models import SupportChatSession, SupportChatMessage, SupportChatStatus, SupportChatTopic
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """Описує клас `UserFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = User
        skip_postgeneration_save = True
    username = factory.Sequence(lambda n: f'user{n}')
    first_name = 'Іван'
    last_name = factory.Sequence(lambda n: f'Петренко{n}')
    middle_name = 'Іванович'
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    pending_email = ''
    phone = factory.Sequence(lambda n: f'+380500000{n:03d}')
    email_verified = True
    discount = 0
    birth_date = None
    preferred_contact_channel = ''

    @factory.post_generation
    def password(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        """Виконує логіку `password`.

Args:
    create: Вхідний параметр `create`.
    extracted: Вхідний параметр `extracted`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        password = extracted or 'testpass123'
        self.set_password(password)
        if create:
            self.save()

class AnalysisFactory(factory.django.DjangoModelFactory):
    """Описує клас `AnalysisFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Analysis
    name = factory.Sequence(lambda n: f'Аналіз {n}')
    what_to_check = 'Загальні показники'
    disease = 'Профілактика'
    for_whom = 'Для дорослих'
    biomaterial = 'Кров'
    duration_days = 2
    price = '450.00'
    is_active = True

class ClinicInfoFactory(factory.django.DjangoModelFactory):
    """Описує клас `ClinicInfoFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = ClinicInfo
    title = 'Про клініку Avelon Healthcare'
    description = 'Сучасна багатопрофільна клініка.'
    goals = 'Надавати якісну медичну допомогу.'
    values = 'Турбота, професіоналізм, довіра.'
    achievements = 'Понад 1000 задоволених пацієнтів.'
    image = None

class ContactInfoFactory(factory.django.DjangoModelFactory):
    """Описує клас `ContactInfoFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = ContactInfo
    address = 'м. Київ, вул. Хрещатик, 1'
    work_schedule = 'Пн-Пт 08:00-20:00'
    phone_1 = '+380441234567'
    phone_2 = '+380671234567'
    email = 'clinic@example.com'
    google_map_embed_url = 'https://maps.google.com/'
    facebook_url = 'https://facebook.com/avelon'
    instagram_url = 'https://instagram.com/avelon'
    youtube_url = 'https://youtube.com/@avelon'

class PromotionFactory(factory.django.DjangoModelFactory):
    """Описує клас `PromotionFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Promotion
    title = factory.Sequence(lambda n: f'Акція {n}')
    image = None
    description = 'Спеціальна пропозиція для пацієнтів.'
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=30))

class DirectionFactory(factory.django.DjangoModelFactory):
    """Описує клас `DirectionFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Direction
    name = factory.Sequence(lambda n: f'Напрям {n}')
    description = 'Опис медичного напряму'

class DoctorFactory(factory.django.DjangoModelFactory):
    """Описує клас `DoctorFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Doctor
    user = None
    last_name = factory.Sequence(lambda n: f'Лікаренко{n}')
    first_name = 'Іван'
    middle_name = 'Іванович'
    position = 'Лікар-терапевт'
    qualification_category = 'Вища категорія'
    experience_years = 10
    price_from = '500.00'
    price_to = '900.00'
    photo = None
    work_experience_description = 'Має великий досвід роботи.'
    when_to_contact = 'При перших симптомах захворювання.'
    education = 'НМУ ім. Богомольця'
    licenses = None

    @factory.post_generation
    def directions(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        """Виконує логіку `directions`.

Args:
    create: Вхідний параметр `create`.
    extracted: Вхідний параметр `extracted`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        if not create:
            return
        if extracted:
            for direction in extracted:
                self.directions.add(direction)
        else:
            self.directions.add(DirectionFactory())

class DoctorWorkDayFactory(factory.django.DjangoModelFactory):
    """Описує клас `DoctorWorkDayFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = DoctorWorkDay
    doctor = factory.SubFactory(DoctorFactory)
    work_date = factory.LazyFunction(lambda: date.today() + timedelta(days=1))
    appointment_duration_minutes = 30
    direction = factory.SubFactory(DirectionFactory)

    @factory.post_generation
    def sync_doctor_direction(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        """Виконує логіку `sync_doctor_direction`.

Args:
    create: Вхідний параметр `create`.
    extracted: Вхідний параметр `extracted`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        if not create:
            return
        self.doctor.directions.add(self.direction)

class DoctorWorkPeriodFactory(factory.django.DjangoModelFactory):
    """Описує клас `DoctorWorkPeriodFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = DoctorWorkPeriod
    workday = factory.SubFactory(DoctorWorkDayFactory)
    start_time = time(9, 0)
    end_time = time(12, 0)

class AppointmentFactory(factory.django.DjangoModelFactory):
    """Описує клас `AppointmentFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Appointment
    user = factory.SubFactory(UserFactory)
    last_name = 'Петренко'
    first_name = 'Іван'
    middle_name = 'Іванович'
    phone = factory.Sequence(lambda n: f'+380670000{n:03d}')
    email = factory.Sequence(lambda n: f'appointment{n}@example.com')
    direction = factory.SubFactory(DirectionFactory)
    doctor = factory.SubFactory(DoctorFactory)
    appointment_date = factory.LazyFunction(lambda: date.today() + timedelta(days=1))
    appointment_time = time(10, 0)
    description = 'Первинна консультація'
    status = AppointmentStatus.PLANNED
    rejection_reason = ''
    final_conclusion = None

    @factory.post_generation
    def sync_doctor_direction(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        """Виконує логіку `sync_doctor_direction`.

Args:
    create: Вхідний параметр `create`.
    extracted: Вхідний параметр `extracted`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        if not create:
            return
        self.doctor.directions.add(self.direction)

class OrderFactory(factory.django.DjangoModelFactory):
    """Описує клас `OrderFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Order
    user = factory.SubFactory(UserFactory)
    last_name = 'Петренко'
    first_name = 'Іван'
    middle_name = 'Іванович'
    phone = factory.Sequence(lambda n: f'+380680000{n:03d}')
    email = factory.Sequence(lambda n: f'order{n}@example.com')
    status = OrderStatus.NEW
    payment_method = PaymentMethod.CASH
    paid_at = None
    total_price = Decimal('0.00')
    result_file = None
    rejection_reason = ''

class OrderItemFactory(factory.django.DjangoModelFactory):
    """Описує клас `OrderItemFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = OrderItem
    order = factory.SubFactory(OrderFactory)
    analysis = factory.SubFactory(AnalysisFactory)
    price = Decimal('450.00')

class ReviewFactory(factory.django.DjangoModelFactory):
    """Описує клас `ReviewFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Review
    user = factory.SubFactory(UserFactory)
    text = 'Все було чудово, лікар допоміг.'
    clinic_reply = ''

    @factory.lazy_attribute
    def appointment(self) -> Any:
        """Виконує логіку `appointment`.

Returns:
    Any: Результат виконання."""
        return AppointmentFactory(user=self.user, status=AppointmentStatus.COMPLETED)

class SupportChatSessionFactory(factory.django.DjangoModelFactory):
    """Описує клас `SupportChatSessionFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = SupportChatSession
    user = factory.SubFactory(UserFactory)
    guest_name = ''
    guest_email = ''
    topic = SupportChatTopic.OTHER
    initial_description = 'Потрібна допомога з сервісом.'
    operator = None
    status = SupportChatStatus.WAITING
    connected_at = None
    closed_at = None

class SupportChatMessageFactory(factory.django.DjangoModelFactory):
    """Описує клас `SupportChatMessageFactory`."""

    class Meta:
        """Описує клас `Meta`."""
        model = SupportChatMessage
    session = factory.SubFactory(SupportChatSessionFactory)
    author_type = SupportChatMessage.AuthorType.USER
    author_name = 'Користувач'
    text = 'Доброго дня, потрібна консультація.'
