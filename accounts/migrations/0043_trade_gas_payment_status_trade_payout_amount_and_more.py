

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0042_withdrawal_source'),
]

operations=[
migrations.AddField(
model_name='trade',
name='gas_payment_status',
field=models.CharField(default='not_required',max_length=20),
),
migrations.AddField(
model_name='trade',
name='payout_amount',
field=models.DecimalField(blank=True,decimal_places=2,max_digits=18,null=True),
),
migrations.AddField(
model_name='trade',
name='payout_released',
field=models.BooleanField(default=False),
),
migrations.AddField(
model_name='trade',
name='profit_amount',
field=models.DecimalField(blank=True,decimal_places=2,max_digits=18,null=True),
),
]
