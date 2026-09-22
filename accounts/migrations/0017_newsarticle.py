

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0016_referral'),
]

operations=[
migrations.CreateModel(
name='NewsArticle',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=255)),
('url',models.URLField()),
('source',models.CharField(max_length=100)),
('description',models.TextField()),
('published_at',models.DateTimeField()),
],
),
]
