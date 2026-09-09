                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_investor_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='total_investment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
