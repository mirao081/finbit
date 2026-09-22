

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0024_delete_twofactorsettings'),
]

operations=[
migrations.AddField(
model_name='userprofile',
name='recovery_email',
field=models.EmailField(blank=True,max_length=254,null=True),
),
migrations.AddField(
model_name='userprofile',
name='recovery_phone',
field=models.CharField(blank=True,max_length=20,null=True),
),
]
