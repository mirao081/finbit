from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "core",
            "0034_transaction_wallet_currency_alter_transaction_amount_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="investmentplan",
            old_name="days",
            new_name="frequency",
        ),
        migrations.RenameField(
            model_name="investmentplan",
            old_name="total_percentage",
            new_name="total_return",
        ),
    ]