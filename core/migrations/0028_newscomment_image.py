                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_newstag_newscomment_newsitem_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='newscomment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='comments/'),
        ),
    ]
