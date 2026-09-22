

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0028_announcementread'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.AddField(
model_name='userprofile',
name='referrer',
field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='referred_users',to=settings.AUTH_USER_MODEL),
),
]
