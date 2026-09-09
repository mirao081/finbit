                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_investor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='investors/'),
        ),
    ]
