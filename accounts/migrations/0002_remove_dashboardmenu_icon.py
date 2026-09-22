

fromdjango.dbimportmigrations


classMigration(migrations.Migration):

    dependencies=[
('accounts','0001_initial'),
]

operations=[
migrations.RemoveField(
model_name='dashboardmenu',
name='icon',
),
]
