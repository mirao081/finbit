                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_newsitem_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
