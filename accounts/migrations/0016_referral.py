

importdjango.db.models.deletion
fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0015_profit'),
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

operations=[
migrations.CreateModel(
name='Referral',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('created_at',models.DateTimeField(auto_now_add=True)),
('commission_earned',models.DecimalField(decimal_places=2,default=0,max_digits=18)),
('referred_user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='referred_by',to=settings.AUTH_USER_MODEL)),
('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='referrals',to=settings.AUTH_USER_MODEL)),
],
),
]
