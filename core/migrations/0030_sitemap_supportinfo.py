                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('embed_code', models.TextField(help_text='Paste Google Maps iframe embed code here')),
            ],
        ),
        migrations.CreateModel(
            name='SupportInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('call', 'Call Us'), ('email', 'Email Us'), ('visit', 'Visit Us')], max_length=10)),
                ('heading', models.CharField(max_length=50)),
                ('detail_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('detail_line2', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
