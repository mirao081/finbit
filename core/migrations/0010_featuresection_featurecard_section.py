

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0009_remove_featurecard_icon'),
]

operations=[
migrations.CreateModel(
name='FeatureSection',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('heading',models.CharField(max_length=200)),
('subheading',models.CharField(blank=True,max_length=300,null=True)),
],
),
migrations.AddField(
model_name='featurecard',
name='section',
field=models.ForeignKey(default=1,on_delete=django.db.models.deletion.CASCADE,related_name='cards',to='core.featuresection'),
preserve_default=False,
),
]
