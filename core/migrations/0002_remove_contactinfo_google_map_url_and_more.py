from django.db import migrations, models

class Migration(migrations.Migration):
    """Описує клас `Migration`."""
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RemoveField(model_name='contactinfo', name='google_map_url'), migrations.AddField(model_name='contactinfo', name='google_map_embed_url', field=models.TextField(blank=True, verbose_name='Google Maps Embed URL'))]
