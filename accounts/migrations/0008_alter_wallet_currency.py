                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT_TRC20', 'USDT TRC20'), ('USDT_ERC20', 'USDT ERC20')], max_length=20),
        ),
    ]
