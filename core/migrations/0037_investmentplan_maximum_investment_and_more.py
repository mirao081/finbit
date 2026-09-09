                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_investmentplan_total_return'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentplan',
            name='maximum_investment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='investmentplan',
            name='duration',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='investmentplan',
            name='minimum_investment',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
