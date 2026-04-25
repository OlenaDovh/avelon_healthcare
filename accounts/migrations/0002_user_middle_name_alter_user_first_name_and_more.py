from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('accounts', '0001_initial')]
    operations = [migrations.AddField(model_name='user', name='middle_name', field=models.CharField(blank=True, max_length=150, verbose_name='По батькові')), migrations.AlterField(model_name='user', name='first_name', field=models.CharField(max_length=150, verbose_name="Ім'я")), migrations.AlterField(model_name='user', name='is_staff', field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')), migrations.AlterField(model_name='user', name='last_name', field=models.CharField(max_length=150, verbose_name='Прізвище'))]
