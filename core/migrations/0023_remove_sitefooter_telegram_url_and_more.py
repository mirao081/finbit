

fromdjango.dbimportmigrations


classMigration(migrations.Migration):

    dependencies=[
('core','0022_sitefooter'),
]

operations=[
migrations.RemoveField(
model_name='sitefooter',
name='telegram_url',
),
migrations.RemoveField(
model_name='sitefooter',
name='whatsapp_url',
),
]
