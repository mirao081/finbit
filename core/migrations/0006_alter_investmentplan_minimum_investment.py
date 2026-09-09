                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_investmentplan_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentplan',
            name='minimum_investment',
            field=models.CharField(max_length=50),
        ),
    ]
