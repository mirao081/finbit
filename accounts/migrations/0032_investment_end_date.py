                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_alter_deposit_payment_method_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
