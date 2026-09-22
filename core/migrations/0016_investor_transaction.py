

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0015_teammember'),
]

operations=[
migrations.CreateModel(
name='Investor',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('name',models.CharField(max_length=100)),
('picture',models.ImageField(upload_to='investors/')),
],
),
migrations.CreateModel(
name='Transaction',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('date',models.DateTimeField(auto_now_add=True)),
('amount',models.DecimalField(decimal_places=2,max_digits=12)),
('activity_type',models.CharField(choices=[('deposit','Deposit'),('investment','Investment'),('withdrawal','Withdrawal')],max_length=20)),
('investor',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='core.investor')),
],
),
]
