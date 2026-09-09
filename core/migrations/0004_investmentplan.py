                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_sitesettings_about_button_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('return_rate', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=100)),
                ('days', models.PositiveIntegerField()),
                ('total_percentage', models.CharField(max_length=50)),
                ('minimum_investment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
