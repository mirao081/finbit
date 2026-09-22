

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0046_alter_profit_options_profit_investment_and_more'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.CreateModel(
name='RecoveryCode',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('code_hash',models.CharField(max_length=128)),
('used_at',models.DateTimeField(blank=True,null=True)),
('created_at',models.DateTimeField(auto_now_add=True)),
('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='recovery_codes',to=settings.AUTH_USER_MODEL)),
],
options={
'ordering':['created_at'],
},
),
]
