                                             

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_featurecard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featurecard',
            name='icon',
        ),
    ]
