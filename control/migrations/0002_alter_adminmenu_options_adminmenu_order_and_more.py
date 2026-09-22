

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('control','0001_initial'),
]

operations=[
migrations.AlterModelOptions(
name='adminmenu',
options={'ordering':['order']},
),
migrations.AddField(
model_name='adminmenu',
name='order',
field=models.PositiveIntegerField(default=0),
),
migrations.AlterField(
model_name='adminmenu',
name='icon',
field=models.CharField(max_length=50),
),
]
