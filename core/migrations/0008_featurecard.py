

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0007_cryptostat'),
]

operations=[
migrations.CreateModel(
name='FeatureCard',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=100)),
('description',models.TextField()),
('icon',models.CharField(help_text='FontAwesome icon class, e.g. fa-solid fa-shield',max_length=50)),
('is_active',models.BooleanField(default=True)),
],
),
]
