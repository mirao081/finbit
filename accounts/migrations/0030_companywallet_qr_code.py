

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0029_userprofile_referrer'),
]

operations=[
migrations.AddField(
model_name='companywallet',
name='qr_code',
field=models.ImageField(blank=True,null=True,upload_to='company_wallets/'),
),
]
