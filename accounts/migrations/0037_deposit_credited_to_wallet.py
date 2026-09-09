                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_wallet_reserved_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='credited_to_wallet',
            field=models.BooleanField(default=False),
        ),
    ]
