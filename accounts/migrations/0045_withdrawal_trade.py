

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0044_tradegaspayment'),
]

operations=[
migrations.AddField(
model_name='withdrawal',
name='trade',
field=models.OneToOneField(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='withdrawal',to='accounts.trade'),
),
]
