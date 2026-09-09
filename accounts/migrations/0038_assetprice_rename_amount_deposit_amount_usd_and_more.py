                                             

import django.db.models.deletion

from django.db import migrations, models


def copy_investment_amount_to_amount_usd(apps, schema_editor):
    """
    Preserve the old Investment.amount values by copying them
    into the new Investment.amount_usd field before the old
    database column is removed.
    """
    Investment = apps.get_model("accounts", "Investment")

    for investment in Investment.objects.all():
        if investment.amount is not None:
            investment.amount_usd = investment.amount
            investment.save(update_fields=["amount_usd"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0037_deposit_credited_to_wallet"),
        ("core", "0037_investmentplan_maximum_investment_and_more"),
    ]

    operations = [

                                                                   
                     
                                                                   

        migrations.CreateModel(
            name="AssetPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("BTC", "Bitcoin"),
                            ("ETH", "Ethereum"),
                            ("USDT_TRC20", "Tether TRC20"),
                            ("USDT_ERC20", "Tether ERC20"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
                (
                    "usd_price",
                    models.DecimalField(
                        decimal_places=12,
                        default=0,
                        max_digits=30,
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True),
                ),
            ],
        ),

                                                                   
                 
                                                                   

        migrations.RenameField(
            model_name="deposit",
            old_name="amount",
            new_name="amount_usd",
        ),

        migrations.AddField(
            model_name="deposit",
            name="approved_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="deposit",
            name="asset_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="deposit",
            name="exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="deposit",
            name="received_asset_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                help_text=(
                    "Actual amount of cryptocurrency received "
                    "and credited."
                ),
                max_digits=30,
                null=True,
            ),
        ),

                                                                   
                    
                                                                   
         
                    
                                                              
                                          
                                              
         

        migrations.AddField(
            model_name="investment",
            name="amount_usd",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=18,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="investment",
            name="asset_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="investment",
            name="exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="investment",
            name="wallet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="investments",
                to="accounts.wallet",
            ),
        ),

                                                         
        migrations.RunPython(
            copy_investment_amount_to_amount_usd,
            migrations.RunPython.noop,
        ),

                                                            
        migrations.RemoveField(
            model_name="investment",
            name="amount",
        ),

                                                                   
                
                                                                   

        migrations.AddField(
            model_name="wallet",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="wallet",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                null=True,
            ),
        ),

                                                                   
                    
                                                                   

        migrations.RenameField(
            model_name="withdrawal",
            old_name="amount",
            new_name="amount_usd",
        ),

        migrations.RemoveField(
            model_name="withdrawal",
            name="asset",
        ),

        migrations.AddField(
            model_name="withdrawal",
            name="approved_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="withdrawal",
            name="asset_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="withdrawal",
            name="exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=12,
                max_digits=30,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="withdrawal",
            name="wallet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="withdrawals",
                to="accounts.wallet",
            ),
        ),

                                                                   
                                
                                                                   

        migrations.AlterField(
            model_name="deposit",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("BTC", "Bitcoin"),
                    ("ETH", "Ethereum"),
                    ("USDT_TRC20", "Tether TRC20"),
                    ("USDT_ERC20", "Tether ERC20"),
                ],
                max_length=20,
            ),
        ),

        migrations.AlterField(
            model_name="deposit",
            name="plan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="deposits",
                to="core.investmentplan",
            ),
        ),

        migrations.AlterField(
            model_name="investment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                null=True,
            ),
        ),

        migrations.AlterField(
            model_name="investment",
            name="plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="investments",
                to="core.investmentplan",
            ),
        ),

        migrations.AlterField(
            model_name="investment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="investments",
                to="auth.user",
            ),
        ),

        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(
                decimal_places=12,
                default=0,
                max_digits=30,
            ),
        ),

        migrations.AlterField(
            model_name="wallet",
            name="reserved_balance",
            field=models.DecimalField(
                decimal_places=12,
                default=0,
                max_digits=30,
            ),
        ),

                                                                   
                           
                                                                   

        migrations.AddConstraint(
            model_name="wallet",
            constraint=models.UniqueConstraint(
                fields=("user", "currency"),
                name="unique_user_wallet_currency",
            ),
        ),
    ]