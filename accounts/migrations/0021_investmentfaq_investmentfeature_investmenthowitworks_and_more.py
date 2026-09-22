

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0020_profilepage'),
]

operations=[
migrations.CreateModel(
name='InvestmentFAQ',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('question',models.CharField(max_length=300)),
('answer',models.TextField()),
('order',models.PositiveIntegerField(default=0)),
('is_active',models.BooleanField(default=True)),
],
options={
'ordering':['order'],
},
),
migrations.CreateModel(
name='InvestmentFeature',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=150)),
('description',models.TextField()),
('icon',models.CharField(default='✓',max_length=50)),
('order',models.PositiveIntegerField(default=0)),
('is_active',models.BooleanField(default=True)),
],
options={
'ordering':['order'],
},
),
migrations.CreateModel(
name='InvestmentHowItWorks',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('title',models.CharField(max_length=150)),
('description',models.TextField()),
('icon',models.CharField(default='1',max_length=50)),
('order',models.PositiveIntegerField(default=0)),
('is_active',models.BooleanField(default=True)),
],
options={
'ordering':['order'],
},
),
migrations.CreateModel(
name='InvestmentPageContent',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('hero_title',models.CharField(default='Start Your Investment Journey',max_length=200)),
('hero_subtitle',models.TextField(default='Choose an investment plan that matches your goals and invest from your approved balance.')),
('balance_label',models.CharField(default='Available Balance',max_length=100)),
('how_title',models.CharField(default='How Your Investment Works',max_length=200)),
('how_subtitle',models.TextField(default='A simple, transparent process designed to make investing straightforward.')),
('calculator_title',models.CharField(default='Investment Calculator',max_length=200)),
('calculator_subtitle',models.TextField(default='Estimate your potential return before you invest.')),
('security_title',models.CharField(default='Built Around Security & Transparency',max_length=200)),
('security_text',models.TextField(default='Your account information and investment activity are handled through our secure platform.')),
('terms_title',models.CharField(default='Important Investment Information',max_length=200)),
('terms_text',models.TextField(default='Investment returns, durations and conditions vary by plan. Please review the details of each plan carefully before investing.')),
('faq_title',models.CharField(default='Frequently Asked Questions',max_length=200)),
('support_title',models.CharField(default='Need Help Before You Invest?',max_length=200)),
('support_text',models.TextField(default='Our support team is available to help you understand the investment process.')),
('support_button_text',models.CharField(default='Contact Support',max_length=100)),
('updated_at',models.DateTimeField(auto_now=True)),
],
),
migrations.AddField(
model_name='userprofile',
name='name',
field=models.CharField(blank=True,max_length=100,null=True),
),
migrations.AddField(
model_name='userprofile',
name='picture',
field=models.ImageField(blank=True,null=True,upload_to='profile_pics/'),
),
migrations.AddField(
model_name='userprofile',
name='referral_earnings',
field=models.DecimalField(decimal_places=2,default=0.0,max_digits=12),
),
migrations.AddField(
model_name='userprofile',
name='total_investment',
field=models.DecimalField(decimal_places=2,default=0,max_digits=12),
),
]
