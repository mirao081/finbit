                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_threestepsection_stepitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subheading', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='testimonials/')),
                ('stars', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.AlterField(
            model_name='stepitem',
            name='icon',
            field=models.CharField(help_text="FontAwesome icon class, e.g. 'fa-user', 'fa-dollar-sign', 'fa-wallet'", max_length=50),
        ),
    ]
