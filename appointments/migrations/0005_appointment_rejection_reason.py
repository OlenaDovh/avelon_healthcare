from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('appointments', '0004_remove_appointment_full_name_and_more')]
    operations = [migrations.AddField(model_name='appointment', name='rejection_reason', field=models.TextField(blank=True, verbose_name='Причина відхилення'))]
