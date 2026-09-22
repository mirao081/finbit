

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
('accounts','0021_investmentfaq_investmentfeature_investmenthowitworks_and_more'),
]

operations=[
migrations.CreateModel(
name='SecurityCenterContent',
fields=[
('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
('hero_title',models.CharField(default='Security Center',max_length=200)),
('hero_subtitle',models.TextField(default='Protect your account with advanced security, verification, and activity controls.')),
('twofa_title',models.CharField(default='Two-Factor Authentication',max_length=200)),
('twofa_text',models.TextField(default='Add an extra layer of protection to your account using two-factor authentication.')),
('compliance_title',models.CharField(default='Compliance & Verification',max_length=200)),
('compliance_text',models.TextField(default='Complete identity verification to help keep your account secure and compliant.')),
('activity_title',models.CharField(default='Device & Activity',max_length=200)),
('activity_text',models.TextField(default='Review recent login activity and manage active sessions connected to your account.')),
('controls_title',models.CharField(default='User Controls',max_length=200)),
('controls_text',models.TextField(default='Manage your password, recovery options, and API access from one secure location.')),
('alerts_title',models.CharField(default='Security Alerts',max_length=200)),
('alerts_text',models.TextField(default='Monitor suspicious login attempts, unusual activity, and withdrawal security alerts.')),
('updated_at',models.DateTimeField(auto_now=True)),
],
),
]
