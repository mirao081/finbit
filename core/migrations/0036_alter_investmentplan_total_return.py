from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "core",
            "0035_rename_days_investmentplan_frequency_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmentplan",
            name="total_return",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
            ),
        ),
    ]