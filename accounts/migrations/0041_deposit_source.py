

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0040_trade'),
]

operations=[
migrations.AddField(
model_name='deposit',
name='source',
field=models.CharField(default='deposit',max_length=30),
),
]
