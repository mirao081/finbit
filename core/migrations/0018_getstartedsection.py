

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('core','0017_investor_total_investment'),
]

operations=[
migrations.CreateModel(
name='GetStartedSection',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=255)),
('subtitle',models.TextField()),
('button_text',models.CharField(default='Join Us',max_length=50)),
('button_link',models.URLField(default='#')),
],
),
]
