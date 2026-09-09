                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_newssection_newsitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteFooter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='footer/')),
                ('whatsapp_url', models.URLField(blank=True, null=True)),
                ('telegram_url', models.URLField(blank=True, null=True)),
                ('year', models.CharField(default='2020', max_length=4)),
                ('company_name', models.CharField(default='Finbit', max_length=100)),
            ],
        ),
    ]
