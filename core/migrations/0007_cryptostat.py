

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0006_alter_investmentplan_minimum_investment'),
]

operations=[
migrations.CreateModel(
name='CryptoStat',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('label',models.CharField(max_length=100)),
('value',models.CharField(max_length=100)),
],
),
]
