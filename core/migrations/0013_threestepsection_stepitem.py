

importdjango.db.models.deletion
fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0012_profitcalculatorsection'),
]

operations=[
migrations.CreateModel(
name='ThreeStepSection',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('heading',models.CharField(max_length=200)),
('subheading',models.CharField(blank=True,max_length=300,null=True)),
],
),
migrations.CreateModel(
name='StepItem',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('number',models.IntegerField()),
('title',models.CharField(max_length=100)),
('icon',models.CharField(help_text="FontAwesome icon class, e.g. 'fa-user'",max_length=50)),
('section',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='steps',to='core.threestepsection')),
],
),
]
