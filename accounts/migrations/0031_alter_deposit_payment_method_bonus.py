

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0030_companywallet_qr_code'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.AlterField(
model_name='deposit',
name='payment_method',
field=models.CharField(choices=[('BTC','Bitcoin'),('ETH','Ethereum'),('USDT_TRC20','Tether TRC20'),('USDT_ERC20','Tether ERC20')],default='BTC',max_length=20),
),
migrations.CreateModel(
name='Bonus',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('amount',models.DecimalField(decimal_places=2,max_digits=18)),
('bonus_type',models.CharField(choices=[('welcome','Welcome Bonus'),('investment','Investment Bonus'),('promotion','Promotional Bonus'),('manual','Manual Bonus')],max_length=20)),
('status',models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')],default='pending',max_length=20)),
('description',models.CharField(blank=True,max_length=255,null=True)),
('created_at',models.DateTimeField(auto_now_add=True)),
('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='bonuses',to=settings.AUTH_USER_MODEL)),
],
),
]
