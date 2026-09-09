                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sitesettings_hero_background_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='about_button_link',
            field=models.CharField(default='#', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_button_text',
            field=models.CharField(default='More Info', max_length=50),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_content',
            field=models.TextField(default='We are building the future of finance with blockchain innovation.'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='about_heading',
            field=models.CharField(default='About Us', max_length=150),
        ),
    ]
