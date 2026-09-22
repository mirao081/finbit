

fromdjango.dbimportmigrations


classMigration(migrations.Migration):

    dependencies=[
('core','0008_featurecard'),
]

operations=[
migrations.RemoveField(
model_name='featurecard',
name='icon',
),
]
