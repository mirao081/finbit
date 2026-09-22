

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0014_testimonial_alter_stepitem_icon'),
]

operations=[
migrations.CreateModel(
name='TeamMember',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('name',models.CharField(max_length=100)),
('position',models.CharField(max_length=150)),
('image',models.ImageField(upload_to='team_members/')),
],
),
]
