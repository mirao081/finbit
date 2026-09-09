                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_deposit_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='payment_method',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDTTRC20', 'Tether TRC20'), ('USDTERC20', 'Tether ERC20')], default='BTC', max_length=20),
        ),
    ]
