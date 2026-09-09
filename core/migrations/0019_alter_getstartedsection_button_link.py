                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_getstartedsection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getstartedsection',
            name='button_link',
            field=models.CharField(default='#'),
        ),
    ]
