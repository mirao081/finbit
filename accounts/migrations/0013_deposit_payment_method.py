                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='payment_method',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT', 'Tether')], default='BTC', max_length=10),
        ),
    ]
