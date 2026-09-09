                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_newsarticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Support Center', max_length=200)),
                ('content', models.TextField(help_text='Main support content')),
                ('contact_email', models.EmailField(default='support@example.com', max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='NewsArticle',
        ),
    ]
