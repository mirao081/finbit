

fromdjango.dbimportmigrations


classMigration(migrations.Migration):

    dependencies=[
('accounts','0023_twofactorsettings'),
]

operations=[
migrations.DeleteModel(
name='TwoFactorSettings',
),
]
