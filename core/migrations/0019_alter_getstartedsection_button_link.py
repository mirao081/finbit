

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0018_getstartedsection'),
]

operations=[
migrations.AlterField(
model_name='getstartedsection',
name='button_link',
field=models.CharField(default='#'),
),
]
