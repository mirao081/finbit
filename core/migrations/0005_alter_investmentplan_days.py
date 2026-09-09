                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_investmentplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentplan',
            name='days',
            field=models.CharField(max_length=50),
        ),
    ]
