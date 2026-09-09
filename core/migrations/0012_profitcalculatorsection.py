                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_featurecard_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitCalculatorSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('subheading', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]
