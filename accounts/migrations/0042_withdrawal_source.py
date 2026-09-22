

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0041_deposit_source'),
]

operations=[
migrations.AddField(
model_name='withdrawal',
name='source',
field=models.CharField(default='withdrawal',max_length=30),
),
]
