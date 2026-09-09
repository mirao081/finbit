                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_rename_contact_email_supportpage_email_support_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(default='My Profile', max_length=200)),
                ('subheading', models.CharField(default='Manage your account, investments, security and wallets', max_length=300)),
                ('personal_info_heading', models.CharField(default='Personal Information', max_length=200)),
                ('investment_summary_heading', models.CharField(default='Investment Summary', max_length=200)),
                ('recent_investments_heading', models.CharField(default='Recent Investments', max_length=200)),
                ('quick_actions_heading', models.CharField(default='Quick Actions', max_length=200)),
                ('referral_heading', models.CharField(default='Referral Program', max_length=200)),
                ('account_settings_heading', models.CharField(default='Account Settings', max_length=200)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
