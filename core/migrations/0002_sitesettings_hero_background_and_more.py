                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero_background',
            field=models.ImageField(blank=True, null=True, upload_to='hero/'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_button_text',
            field=models.CharField(default='Sign Up', max_length=50),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_subtitle',
            field=models.CharField(default='Your modern financial platform.', max_length=255),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_title_gold',
            field=models.CharField(default='Finbit', max_length=100),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_title_white',
            field=models.CharField(default='Welcome to', max_length=100),
        ),
    ]
