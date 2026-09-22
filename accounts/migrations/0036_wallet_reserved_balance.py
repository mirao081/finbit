

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0035_alter_recoveryotp_purpose'),
]

operations=[
migrations.AddField(
model_name='wallet',
name='reserved_balance',
field=models.DecimalField(decimal_places=8,default=0,max_digits=18),
),
]
