

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0031_compliancenotice_newslettersignup_sociallink'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.AddField(
model_name='investor',
name='user',
field=models.OneToOneField(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL),
),
]
