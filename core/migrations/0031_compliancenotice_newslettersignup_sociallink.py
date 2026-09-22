

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0030_sitemap_supportinfo'),
]

operations=[
migrations.CreateModel(
name='ComplianceNotice',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=255)),
('description',models.TextField()),
],
),
migrations.CreateModel(
name='NewsletterSignup',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('email',models.EmailField(max_length=254,unique=True)),
('created_at',models.DateTimeField(auto_now_add=True)),
],
),
migrations.CreateModel(
name='SocialLink',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('platform',models.CharField(choices=[('twitter','Twitter'),('telegram','Telegram'),('linkedin','LinkedIn'),('facebook','Facebook')],max_length=20)),
('url',models.URLField()),
],
),
]
