                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_paymentsection_paymentmethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(default='Our Latest News', max_length=200)),
                ('subheading', models.CharField(default='Stay updated with our latest updates.', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='news/')),
                ('subheading', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('content_title', models.CharField(max_length=200)),
                ('content_preview', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='core.newssection')),
            ],
        ),
    ]
