

importdjango.db.models.deletion

fromdjango.confimportsettings
fromdjango.dbimportmigrations,models


defcopy_transaction_legacy_data(apps,schema_editor):
    """
    Preserve legacy Transaction data before the old fields are removed.

    Old fields:
        amount
        activity_type
        wallet_currency

    New fields:
        usd_value
        transaction_type
        wallet

    We deliberately do NOT guess asset_amount, exchange_rate,
    or direction for historical records.
    """

Transaction=apps.get_model("core","Transaction")
Wallet=apps.get_model("accounts","Wallet")

valid_transaction_types={
"deposit",
"investment",
"withdrawal",
"profit",
"bonus",
"referral",
"admin_credit",
"admin_debit",
"fee",
"exchange",
}

fortransactioninTransaction.objects.all():

        update_fields=[]





iftransaction.amountisnotNone:
            transaction.usd_value=transaction.amount
update_fields.append("usd_value")





iftransaction.activity_type:
            old_type=str(transaction.activity_type).strip().lower()

ifold_typeinvalid_transaction_types:
                transaction.transaction_type=old_type
update_fields.append("transaction_type")












iftransaction.wallet_currency:

            try:
                investor=(
Transaction.objects
.select_related("investor")
.get(pk=transaction.pk)
.investor
)

ifinvestorandinvestor.user_id:

                    wallet=Wallet.objects.filter(
user_id=investor.user_id,
currency=transaction.wallet_currency,
).first()

ifwallet:
                        transaction.wallet_id=wallet.id
update_fields.append("wallet")

exceptException:


                pass





ifupdate_fields:
            transaction.save(update_fields=update_fields)


classMigration(migrations.Migration):

    dependencies=[
(
"accounts",
"0038_assetprice_rename_amount_deposit_amount_usd_and_more",
),
(
"core",
"0037_investmentplan_maximum_investment_and_more",
),
migrations.swappable_dependency(
settings.AUTH_USER_MODEL
),
]

operations=[





migrations.AddField(
model_name="transaction",
name="asset_amount",
field=models.DecimalField(
blank=True,
decimal_places=12,
max_digits=30,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="description",
field=models.CharField(
blank=True,
max_length=255,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="direction",
field=models.CharField(
blank=True,
choices=[
("credit","Credit"),
("debit","Debit"),
],
max_length=10,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="exchange_rate",
field=models.DecimalField(
blank=True,
decimal_places=12,
max_digits=30,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="reference",
field=models.CharField(
blank=True,
max_length=100,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="transaction_type",
field=models.CharField(
blank=True,
choices=[
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
],
max_length=30,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="usd_value",
field=models.DecimalField(
blank=True,
decimal_places=2,
max_digits=18,
null=True,
),
),

migrations.AddField(
model_name="transaction",
name="wallet",
field=models.ForeignKey(
blank=True,
null=True,
on_delete=django.db.models.deletion.PROTECT,
related_name="transactions",
to="accounts.wallet",
),
),





migrations.RunPython(
copy_transaction_legacy_data,
migrations.RunPython.noop,
),





migrations.RemoveField(
model_name="transaction",
name="activity_type",
),

migrations.RemoveField(
model_name="transaction",
name="amount",
),

migrations.RemoveField(
model_name="transaction",
name="wallet_currency",
),





migrations.AlterField(
model_name="transaction",
name="investor",
field=models.ForeignKey(
on_delete=django.db.models.deletion.PROTECT,
related_name="transactions",
to="core.investor",
),
),
]