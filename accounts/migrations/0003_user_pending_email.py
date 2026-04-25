from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('accounts', '0002_user_middle_name_alter_user_first_name_and_more')]
    operations = [migrations.AddField(model_name='user', name='pending_email', field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Нова електронна пошта (очікує підтвердження)'))]
