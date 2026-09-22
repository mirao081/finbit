

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0010_featuresection_featurecard_section'),
]

operations=[
migrations.AlterField(
model_name='featurecard',
name='section',
field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='cards',to='core.featuresection'),
),
]
