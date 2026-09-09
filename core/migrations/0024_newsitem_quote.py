                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_remove_sitefooter_telegram_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='quote',
            field=models.TextField(blank=True, null=True),
        ),
    ]
