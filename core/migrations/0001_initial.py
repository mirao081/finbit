

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    initial=True

dependencies=[
]

operations=[
migrations.CreateModel(
name='MenuItem',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=100)),
('url_name',models.CharField(max_length=100)),
('order',models.PositiveIntegerField(default=0)),
('is_active',models.BooleanField(default=True)),
],
options={
'ordering':['order'],
},
),
migrations.CreateModel(
name='SiteSettings',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('site_name',models.CharField(default='Finbit',max_length=100)),
('logo',models.ImageField(blank=True,null=True,upload_to='logos/')),
('favicon',models.ImageField(blank=True,null=True,upload_to='favicons/')),
],
),
]
