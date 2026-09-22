

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0009_companywallet_deposit'),
('core','0035_rename_days_investmentplan_frequency_and_more'),
]

operations=[
migrations.RemoveField(
model_name='deposit',
name='company_wallet',
),
migrations.RemoveField(
model_name='deposit',
name='currency',
),
migrations.AddField(
model_name='deposit',
name='plan',
field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='deposits',to='core.investmentplan'),
),
migrations.AlterField(
model_name='deposit',
name='amount',
field=models.DecimalField(decimal_places=2,max_digits=18),
),
]
