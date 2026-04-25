import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('accounts', '0003_user_pending_email')]
    operations = [migrations.AlterField(model_name='user', name='discount', field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Знижка, %'))]
