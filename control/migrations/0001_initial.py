

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    initial=True

dependencies=[
]

operations=[
migrations.CreateModel(
name='AdminDashboardSettings',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(default='Finbit Admin Dashboard',max_length=100)),
('logo',models.ImageField(blank=True,null=True,upload_to='admindash/images/')),
],
),
migrations.CreateModel(
name='AdminMenu',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('name',models.CharField(max_length=50)),
('icon',models.CharField(help_text="FontAwesome icon class, e.g. 'fas fa-chart-line'",max_length=50)),
('url_name',models.CharField(max_length=100)),
],
),
]
