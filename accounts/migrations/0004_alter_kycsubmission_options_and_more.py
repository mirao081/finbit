

fromdjango.dbimportmigrations


classMigration(migrations.Migration):

    dependencies=[
('accounts','0003_kycsubmission'),
]

operations=[
migrations.AlterModelOptions(
name='kycsubmission',
options={},
),
migrations.RemoveField(
model_name='kycsubmission',
name='order',
),
]
