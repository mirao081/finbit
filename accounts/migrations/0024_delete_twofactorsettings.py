                                             

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_twofactorsettings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TwoFactorSettings',
        ),
    ]
