

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0034_recoveryotp'),
]

operations=[
migrations.AlterField(
model_name='recoveryotp',
name='purpose',
field=models.CharField(choices=[('recovery_authorization','Recovery Change Authorization'),('recovery_change','Recovery Information Change')],max_length=30),
),
]
