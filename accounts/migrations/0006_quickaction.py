                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_userprofile_referral_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('action_type', models.CharField(choices=[('deposit', 'Deposit'), ('investment', 'Start Investment'), ('withdrawal', 'Withdraw')], max_length=20)),
                ('url_name', models.CharField(help_text='Django URL name for this action', max_length=50)),
                ('icon', models.CharField(default='fa-solid fa-bolt', max_length=50)),
            ],
        ),
    ]
