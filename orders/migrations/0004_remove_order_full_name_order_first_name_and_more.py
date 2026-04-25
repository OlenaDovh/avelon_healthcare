from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('orders', '0003_order_rejection_reason')]
    operations = [migrations.RemoveField(model_name='order', name='full_name'), migrations.AddField(model_name='order', name='first_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name="Ім'я")), migrations.AddField(model_name='order', name='last_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name='Прізвище')), migrations.AddField(model_name='order', name='middle_name', field=models.CharField(blank=True, default='', max_length=150, verbose_name='По батькові'))]
