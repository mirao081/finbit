                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_alter_adminmenu_options_adminmenu_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminmenu',
            name='icon',
            field=models.CharField(help_text="FontAwesome icon class, e.g. 'fas fa-chart-line'", max_length=50),
        ),
    ]
