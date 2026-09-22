fromdjango.dbimportmodels
fromdjango.contrib.auth.modelsimportUser

classSiteSettings(models.Model):
    site_name=models.CharField(max_length=100,default='Finbit')
logo=models.ImageField(upload_to='logos/',null=True,blank=True)
favicon=models.ImageField(upload_to='favicons/',null=True,blank=True)
hero_title_white=models.CharField(max_length=100,default="Welcome to")
hero_title_gold=models.CharField(max_length=100,default="Finbit")
hero_subtitle=models.CharField(max_length=255,default="Your modern financial platform.")
hero_button_text=models.CharField(max_length=50,default="Sign Up")
hero_background=models.ImageField(upload_to="hero/",null=True,blank=True)
about_heading=models.CharField(max_length=150,default="About Us")
about_content=models.TextField(default="We are building the future of finance with blockchain innovation.")
about_button_text=models.CharField(max_length=50,default="More Info")
about_button_link=models.CharField(max_length=200,default="#")

def__str__(self):
        returnself.site_name


classMenuItem(models.Model):
    title=models.CharField(max_length=100)
url_name=models.CharField(max_length=100)
order=models.PositiveIntegerField(default=0)
is_active=models.BooleanField(default=True)

classMeta:
        ordering=['order']

def__str__(self):
        returnself.title


classInvestmentPlan(models.Model):
    name=models.CharField(max_length=100)
return_rate=models.CharField(max_length=50)
frequency=models.CharField(max_length=50)
duration=models.CharField(max_length=50)
total_return=models.CharField(max_length=100,null=True,blank=True)
minimum_investment=models.DecimalField(max_digits=12,decimal_places=2)
maximum_investment=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)

def__str__(self):
        returnstr(self.name)


classCryptoStat(models.Model):
    label=models.CharField(max_length=100)
value=models.CharField(max_length=100)

def__str__(self):
        returnf"{self.label}: {self.value}"


classFeatureSection(models.Model):
    heading=models.CharField(max_length=200)
subheading=models.CharField(max_length=300,blank=True,null=True)

def__str__(self):
        returnself.heading


classFeatureCard(models.Model):
    section=models.ForeignKey(
FeatureSection,
on_delete=models.CASCADE,
related_name="cards",
null=True,
blank=True
)
title=models.CharField(max_length=100)
description=models.TextField()
is_active=models.BooleanField(default=True)

def__str__(self):
        returnself.title

classProfitCalculatorSection(models.Model):
    heading=models.CharField(max_length=200)
subheading=models.CharField(max_length=300,blank=True,null=True)

def__str__(self):
        returnself.heading

classThreeStepSection(models.Model):
    heading=models.CharField(max_length=200)
subheading=models.CharField(max_length=300,blank=True,null=True)

def__str__(self):
        returnself.heading


classStepItem(models.Model):
    section=models.ForeignKey(ThreeStepSection,on_delete=models.CASCADE,related_name="steps")
number=models.IntegerField()
title=models.CharField(max_length=100)
icon=models.CharField(
max_length=50,
help_text="FontAwesome icon class, e.g. 'fa-user', 'fa-dollar-sign', 'fa-wallet'"
)

def__str__(self):
        returnf"{self.number} - {self.title}"

models

classTestimonial(models.Model):
    subheading=models.CharField(max_length=255)
name=models.CharField(max_length=100)
position=models.CharField(max_length=100)
image=models.ImageField(upload_to='testimonials/')
stars=models.PositiveSmallIntegerField(default=5)

def__str__(self):
        returnf"{self.name} - {self.position}"

classTeamMember(models.Model):
    name=models.CharField(max_length=100)
position=models.CharField(max_length=150)
image=models.ImageField(upload_to="team_members/")

def__str__(self):
        returnself.name

classInvestor(models.Model):
    user=models.OneToOneField(
User,
on_delete=models.CASCADE,
null=True,
blank=True
)
name=models.CharField(max_length=100)
picture=models.ImageField(
upload_to="investors/",
blank=True,
null=True
)
total_investment=models.DecimalField(
max_digits=12,
decimal_places=2,
default=0
)

def__str__(self):
        returnself.name

classTransaction(models.Model):
    TYPE_CHOICES=[
("deposit","Deposit"),
("investment","Investment"),
("withdrawal","Withdrawal"),
("profit","Profit"),
("bonus","Bonus"),
("referral","Referral Commission"),
("admin_credit","Admin Credit"),
("admin_debit","Admin Debit"),
("fee","Fee"),
("exchange","Exchange"),
]

DIRECTION_CHOICES=[
("credit","Credit"),
("debit","Debit"),
]

investor=models.ForeignKey(
Investor,
on_delete=models.PROTECT,
related_name="transactions",
)

wallet=models.ForeignKey(
"accounts.Wallet",
on_delete=models.PROTECT,
related_name="transactions",
null=True,
blank=True,
)

transaction_type=models.CharField(
max_length=30,
choices=TYPE_CHOICES,
null=True,
blank=True,
)

direction=models.CharField(
max_length=10,
choices=DIRECTION_CHOICES,
null=True,
blank=True,
)

asset_amount=models.DecimalField(
max_digits=30,
decimal_places=12,
null=True,
blank=True,
)

usd_value=models.DecimalField(
max_digits=18,
decimal_places=2,
null=True,
blank=True,
)

exchange_rate=models.DecimalField(
max_digits=30,
decimal_places=12,
null=True,
blank=True,
)

reference=models.CharField(
max_length=100,
blank=True,
null=True,
)

description=models.CharField(
max_length=255,
blank=True,
null=True,
)

date=models.DateTimeField(
auto_now_add=True,
)


classGetStartedSection(models.Model):
    title=models.CharField(max_length=255)
subtitle=models.TextField()
button_text=models.CharField(max_length=50,default="Join Us")
button_link=models.CharField(max_length=255,default="#")

def__str__(self):
        returnself.title

classPaymentSection(models.Model):
    heading=models.CharField(max_length=200,default="Payment We Accept")
subheading=models.CharField(max_length=300,default="We support multiple payment methods for your convenience.")

def__str__(self):
        returnself.heading


classPaymentMethod(models.Model):
    section=models.ForeignKey(PaymentSection,on_delete=models.CASCADE,related_name="methods")
name=models.CharField(max_length=100)
icon=models.CharField(
max_length=50,
help_text="FontAwesome icon class, e.g. 'fa-bitcoin', 'fa-ethereum'"
)
is_active=models.BooleanField(default=True)

def__str__(self):
        returnself.name

classNewsSection(models.Model):
    heading=models.CharField(max_length=200,default="Our Latest News")
subheading=models.CharField(max_length=300,default="Stay updated with our latest updates.")

def__str__(self):
        returnself.heading

classNewsCategory(models.Model):
    name=models.CharField(max_length=100)
slug=models.SlugField(unique=True)

def__str__(self):
        returnself.name

classNewsTag(models.Model):
    name=models.CharField(max_length=50)
slug=models.SlugField(unique=True)

def__str__(self):
        returnself.name

classNewsItem(models.Model):
    section=models.ForeignKey(
NewsSection,
on_delete=models.CASCADE,
related_name="news"
)
category=models.ForeignKey(
NewsCategory,
on_delete=models.SET_NULL,
null=True,
blank=True,
related_name="news_items"
)
tags=models.ManyToManyField(
NewsTag,
blank=True,
related_name="news_items"
)

image=models.ImageField(upload_to="news/")
subheading=models.CharField(max_length=200)
author=models.CharField(max_length=100)
date=models.DateField()

content_title=models.CharField(max_length=200)
content_preview=models.TextField()

body=models.TextField(blank=True,null=True)
quote=models.TextField(blank=True,null=True)

is_active=models.BooleanField(default=True)

def__str__(self):
        returnself.subheading



classNewsComment(models.Model):
    news=models.ForeignKey(
NewsItem,
on_delete=models.CASCADE,
related_name="comments"
)

name=models.CharField(max_length=100)
email=models.EmailField()

image=models.ImageField(
upload_to="comments/",
blank=True,
null=True
)

comment=models.TextField()

created_at=models.DateTimeField(auto_now_add=True)

approved=models.BooleanField(default=True)

classMeta:
        ordering=["-created_at"]

def__str__(self):
        returnf"{self.name} - {self.news.subheading}"


classSiteFooter(models.Model):
    logo=models.ImageField(upload_to="footer/",blank=True,null=True)
year=models.CharField(max_length=4,default="2020")
company_name=models.CharField(max_length=100,default="Finbit")

def__str__(self):
        returnf"{self.company_name} Footer"



classContactMessage(models.Model):
    full_name=models.CharField(max_length=150)
email=models.EmailField()
message=models.TextField()
created_at=models.DateTimeField(auto_now_add=True)

def__str__(self):
        returnf"{self.full_name} - {self.email}"


classSiteMap(models.Model):
    address=models.CharField(max_length=255)
embed_code=models.TextField(
help_text="Paste Google Maps iframe embed code here"
)

def__str__(self):
        returnself.address


classSupportInfo(models.Model):
    SUPPORT_TYPES=[
("call","Call Us"),
("email","Email Us"),
("visit","Visit Us"),
]
type=models.CharField(max_length=10,choices=SUPPORT_TYPES)
heading=models.CharField(max_length=50)
detail_line1=models.CharField(max_length=255,blank=True,null=True)
detail_line2=models.CharField(max_length=255,blank=True,null=True)

def__str__(self):
        returnf"{self.get_type_display()} - {self.heading}"

classComplianceNotice(models.Model):
    title=models.CharField(max_length=255)
description=models.TextField()

def__str__(self):
        returnself.title


classSocialLink(models.Model):
    PLATFORM_CHOICES=[
("twitter","Twitter"),
("telegram","Telegram"),
("linkedin","LinkedIn"),
("facebook","Facebook"),
]
platform=models.CharField(max_length=20,choices=PLATFORM_CHOICES)
url=models.URLField()

def__str__(self):
        returnself.platform


classNewsletterSignup(models.Model):
    email=models.EmailField(unique=True)
created_at=models.DateTimeField(auto_now_add=True)

def__str__(self):
        returnself.email