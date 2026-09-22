

fromdjango.dbimportmigrations,models


classMigration(migrations.Migration):

    dependencies=[
("core","0038_remove_transaction_activity_type_and_more"),
]

operations=[
migrations.AlterField(
model_name="getstartedsection",
name="button_link",
field=models.CharField(default="#",max_length=255),
),
]
