

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0022_securitycentercontent'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.CreateModel(
name='TwoFactorSettings',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('is_enabled',models.BooleanField(default=False)),
('secret_key',models.CharField(blank=True,max_length=32,null=True)),
('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL)),
],
),
]
