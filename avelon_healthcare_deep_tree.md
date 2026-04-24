# Глибша структура проєкту Avelon Healthcare

```text
Avelon_healthcare/
├── accounts/  # модуль користувачів, ролей, профілю та авторизації
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── auth.py  # авторизація та реєстрація
│   │   ├── passwords.py  # паролі та відновлення доступу
│   │   ├── profile.py  # профіль користувача
│   │   └── support.py  # логіка для підтримки форма
│   ├── management/  # кастомні Django-команди
│   │   ├── commands/  # команди для запуску через manage.py
│   │   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   │   └── setup_roles.py  # команда налаштування ролей
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   ├── 0002_user_middle_name_alter_user_first_name_and_more.py  # міграція змін БД
│   │   ├── 0003_user_pending_email.py  # міграція змін БД
│   │   ├── 0004_alter_user_discount.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── permissions/  # перевірки прав доступу
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── decorators.py  # декоратори доступу
│   │   └── predicates.py  # умови прав доступу
│   ├── services/  # сервісна бізнес-логіка
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── email_verification.py  # підтвердження email
│   │   └── roles.py  # керування ролями
│   ├── tests/  # автоматичні тести
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── test_decorators.py  # тести відповідної частини
│   │   ├── test_forms.py  # тести відповідної частини
│   │   ├── test_models.py  # тести відповідної частини
│   │   ├── test_permissions.py  # тести відповідної частини
│   │   ├── test_predicates.py  # тести відповідної частини
│   │   ├── test_roles.py  # тести відповідної частини
│   │   ├── test_selectors.py  # тести відповідної частини
│   │   ├── test_services.py  # тести відповідної частини
│   │   ├── test_signals.py  # тести відповідної частини
│   │   ├── test_tokens.py  # тести відповідної частини
│   │   └── test_views.py  # тести відповідної частини
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── auth.py  # авторизація та реєстрація
│   │   ├── passwords.py  # паролі та відновлення доступу
│   │   ├── profile.py  # профіль користувача
│   │   └── support.py  # логіка для підтримки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── backends.py  # кастомна автентифікація
│   ├── constants.py  # константи
│   ├── context_processors.py  # дані для шаблонів
│   ├── models.py  # моделі бази даних
│   ├── selectors.py  # запити/вибірки з БД
│   ├── signals.py  # Django-сигнали
│   ├── tasks.py  # фонові задачі Celery
│   ├── tokens.py  # токени підтвердження/відновлення
│   └── urls.py  # URL-маршрути
├── analysis/  # модуль аналізів та кошика
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── services/  # сервісна бізнес-логіка
│   │   └── cart.py  # логіка кошика аналізів
│   ├── tests/  # автоматичні тести
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── test_context_processors.py  # тести відповідної частини
│   │   ├── test_forms.py  # тести відповідної частини
│   │   ├── test_models.py  # тести відповідної частини
│   │   ├── test_selectors.py  # тести відповідної частини
│   │   ├── test_services.py  # тести відповідної частини
│   │   └── test_views.py  # тести відповідної частини
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── head_manager.py  # інтерфейс головного менеджера
│   │   └── public.py  # публічні сторінки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── context_processors.py  # дані для шаблонів
│   ├── forms.py  # форми Django
│   ├── models.py  # моделі бази даних
│   ├── selectors.py  # запити/вибірки з БД
│   └── urls.py  # URL-маршрути
├── appointments/  # модуль записів на прийом
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── create.py  # створення запису/відгуку
│   │   ├── support.py  # логіка для підтримки
│   │   └── update.py  # оновлення запису
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   ├── 0002_appointment_email_appointment_full_name_and_more.py  # міграція змін БД
│   │   ├── 0003_remove_appointment_full_name_appointment_first_name_and_more.py  # міграція змін БД
│   │   ├── 0004_remove_appointment_full_name_and_more.py  # міграція змін БД
│   │   ├── 0005_appointment_rejection_reason.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── services/  # сервісна бізнес-логіка
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── availability.py  # перевірка доступності часу
│   │   ├── creation.py  # створення запису на прийом
│   │   └── notifications.py  # сповіщення
│   ├── tests/  # автоматичні тести
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── test_ajax_views.py  # тести відповідної частини
│   │   ├── test_forms.py  # тести відповідної частини
│   │   ├── test_models.py  # тести відповідної частини
│   │   ├── test_services.py  # тести відповідної частини
│   │   └── test_views.py  # тести відповідної частини
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── ajax.py  # AJAX-запити
│   │   ├── patient.py  # сторінки пацієнта
│   │   ├── public.py  # публічні сторінки
│   │   └── support.py  # логіка для підтримки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── models.py  # моделі бази даних
│   ├── tasks.py  # фонові задачі Celery
│   └── urls.py  # URL-маршрути
├── avelon_healthcare/  # головна конфігурація Django-проєкту
│   ├── settings/  # налаштування середовищ
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── base.py  # базові налаштування
│   │   ├── local.py  # локальні налаштування
│   │   └── test.py  # тестові налаштування
│   ├── tests/  # автоматичні тести
│   │   └── factories.py  # фабрики тестових даних
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── asgi.py  # ASGI-точка входу
│   ├── celery.py  # ініціалізація Celery
│   ├── urls.py  # URL-маршрути
│   └── wsgi.py  # WSGI-точка входу
├── core/  # загальні сторінки, контакти та утиліти
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   ├── 0002_remove_contactinfo_google_map_url_and_more.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── utils/  # допоміжні функції
│   │   └── email.py  # email-утиліти
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   └── pages.py  # інформаційні сторінки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── models.py  # моделі бази даних
│   ├── tests.py  # базові тести
│   └── urls.py  # URL-маршрути
├── daily_horoscope/  # модуль щоденного гороскопу
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── ai.py  # AI-логіка гороскопу
│   ├── apps.py  # конфігурація застосунку
│   └── services.py  # сервісна логіка
├── doctors/  # модуль лікарів, напрямів і розкладів
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── direction.py  # форма напряму лікаря
│   │   ├── doctor.py  # форма лікаря
│   │   └── schedule.py  # форма розкладу лікаря
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   ├── 0002_doctorworkday_doctorworkperiod_and_more.py  # міграція змін БД
│   │   ├── 0003_doctor_user.py  # міграція змін БД
│   │   ├── 0004_alter_doctor_options_alter_doctorworkday_options_and_more.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── ajax.py  # AJAX-запити
│   │   ├── head_manager.py  # інтерфейс головного менеджера
│   │   └── public.py  # публічні сторінки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── models.py  # моделі бази даних
│   ├── tests.py  # базові тести
│   └── urls.py  # URL-маршрути
├── orders/  # модуль замовлень, оплат і рахунків
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── cancel.py  # скасування замовлення
│   │   ├── public.py  # публічні сторінки
│   │   └── support.py  # логіка для підтримки
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   ├── 0002_order_email_order_full_name_order_paid_at_and_more.py  # міграція змін БД
│   │   ├── 0003_order_rejection_reason.py  # міграція змін БД
│   │   ├── 0004_remove_order_full_name_order_first_name_and_more.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── services/  # сервісна бізнес-логіка
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── checkout.py  # оформлення замовлення
│   │   ├── forms.py  # форми Django
│   │   ├── invoice_pdf.py  # генерація PDF-рахунку
│   │   ├── notifications.py  # сповіщення
│   │   └── payments.py  # платежі
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── patient.py  # сторінки пацієнта
│   │   ├── public.py  # публічні сторінки
│   │   └── support.py  # логіка для підтримки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── models.py  # моделі бази даних
│   ├── tasks.py  # фонові задачі Celery
│   ├── tests.py  # базові тести
│   └── urls.py  # URL-маршрути
├── reviews/  # модуль відгуків
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── create.py  # створення запису/відгуку
│   │   └── reply.py  # відповідь на відгук
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── public.py  # публічні сторінки
│   │   └── support.py  # логіка для підтримки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── apps.py  # конфігурація застосунку
│   ├── models.py  # моделі бази даних
│   ├── tests.py  # базові тести
│   └── urls.py  # URL-маршрути
├── support_chat/  # модуль онлайн-чату підтримки
│   ├── forms/  # форми для введення й валідації даних
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   └── start.py  # початок чату
│   ├── migrations/  # міграції бази даних
│   │   ├── 0001_initial.py  # міграція змін БД
│   │   └── __init__.py  # позначає папку як Python-пакет
│   ├── views/  # представлення/контролери
│   │   ├── __init__.py  # позначає папку як Python-пакет
│   │   ├── operator.py  # інтерфейс оператора
│   │   └── public.py  # публічні сторінки
│   ├── __init__.py  # позначає папку як Python-пакет
│   ├── admin.py  # налаштування Django Admin
│   ├── consumers.py  # WebSocket-consumer
│   ├── models.py  # моделі бази даних
│   ├── routing.py  # WebSocket-маршрути
│   ├── services.py  # сервісна логіка
│   └── urls.py  # URL-маршрути
├── conftest.py  # спільні pytest-фікстури
├── manage.py  # головний файл запуску Django-команд
└── pytest.ini  # конфігурація pytest
```
