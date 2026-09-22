

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0018_supportpage_delete_newsarticle'),
]

operations=[
migrations.RenameField(
model_name='supportpage',
old_name='contact_email',
new_name='email_support',
),
migrations.RenameField(
model_name='supportpage',
old_name='title',
new_name='heading',
),
migrations.RenameField(
model_name='supportpage',
old_name='contact_phone',
new_name='phone_support',
),
migrations.RemoveField(
model_name='supportpage',
name='content',
),
migrations.AddField(
model_name='supportpage',
name='account_help_text',
field=models.TextField(default='Our support team is here to help you with deposits, withdrawals, wallet settings, investments, verification, and other account-related questions.'),
),
migrations.AddField(
model_name='supportpage',
name='articles_text',
field=models.TextField(default="We're currently preparing helpful guides and FAQs. Please check back soon."),
),
migrations.AddField(
model_name='supportpage',
name='intro_text',
field=models.TextField(blank=True,null=True),
),
migrations.AddField(
model_name='supportpage',
name='live_chat_available',
field=models.BooleanField(default=True),
),
]
