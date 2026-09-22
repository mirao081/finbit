

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0006_quickaction'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.CreateModel(
name='Wallet',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('currency',models.CharField(choices=[('BTC','Bitcoin'),('ETH','Ethereum'),('USDT','Tether'),('USD','US Dollar')],max_length=10)),
('balance',models.DecimalField(decimal_places=8,default=0,max_digits=18)),
('address',models.CharField(blank=True,max_length=255,null=True)),
('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='wallets',to=settings.AUTH_USER_MODEL)),
],
),
]
