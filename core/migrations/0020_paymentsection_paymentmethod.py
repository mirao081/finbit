                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_getstartedsection_button_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(default='Payment We Accept', max_length=200)),
                ('subheading', models.CharField(default='We support multiple payment methods for your convenience.', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.CharField(help_text="FontAwesome icon class, e.g. 'fa-bitcoin', 'fa-ethereum'", max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='methods', to='core.paymentsection')),
            ],
        ),
    ]
