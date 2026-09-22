

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0039_notification'),
('core','0038_remove_transaction_activity_type_and_more'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.CreateModel(
name='Trade',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('historical_plan_name',models.CharField(blank=True,max_length=100,null=True)),
('result',models.CharField(choices=[('win','Win'),('lose','Lose')],max_length=10)),
('gas_fee',models.DecimalField(blank=True,decimal_places=2,max_digits=10,null=True)),
('created_at',models.DateTimeField(auto_now_add=True)),
('deposit',models.OneToOneField(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='trade',to='accounts.deposit')),
('plan',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,to='core.investmentplan')),
('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL)),
],
),
]
