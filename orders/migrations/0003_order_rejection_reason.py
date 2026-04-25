from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('orders', '0002_order_email_order_full_name_order_paid_at_and_more')]
    operations = [migrations.AddField(model_name='order', name='rejection_reason', field=models.TextField(blank=True, verbose_name='Причина відхилення'))]
