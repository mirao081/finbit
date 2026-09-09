                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_investor_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='wallet_currency',
            field=models.CharField(blank=True, choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT_TRC20', 'USDT TRC20'), ('USDT_ERC20', 'USDT ERC20')], help_text='Currency involved in this transaction', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='core.investor'),
        ),
    ]
