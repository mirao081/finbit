fromdjango.core.management.baseimportBaseCommand
fromdjango.dbimporttransaction
fromdjango.utilsimporttimezone

fromaccounts.modelsimportInvestment,Wallet
fromaccounts.notificationsimportnotify_investment_completed
fromcore.modelsimportInvestor,Transaction


classCommand(BaseCommand):

    help=(
"Complete finite investments whose end date has elapsed, "
"return the original principal, and notify the user."
)

defhandle(self,*args,**options):

        now=timezone.now()

investments=(
Investment.objects
.select_related("user","plan","wallet")
.filter(
status="active",
end_date__isnull=False,
end_date__lte=now,
)
.order_by("end_date")
)

completed_count=0

forinvestmentininvestments:

            try:

                withtransaction.atomic():

                    locked_investment=(
Investment.objects
.select_for_update()
.select_related(
"user",
"plan",
)
.filter(
pk=investment.pk,
status="active",
end_date__isnull=False,
end_date__lte=now,
)
.first()
)

ifnotlocked_investment:
                        continue

if(
notlocked_investment.wallet_id
ornotlocked_investment.asset_amount
orlocked_investment.asset_amount<=0
):
                        self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id} "
f"could not be completed because "
f"its wallet or principal amount "
f"is invalid."
)
)
continue

wallet=(
Wallet.objects
.select_for_update()
.get(
pk=locked_investment.wallet_id
)
)

maturity_reference=(
f"INV-MATURITY-{locked_investment.id}"
)

existing_transaction=(
Transaction.objects
.filter(
reference=maturity_reference
)
.first()
)

ifnotexisting_transaction:

                        investor,_=(
Investor.objects
.get_or_create(
user=locked_investment.user,
defaults={
"name":(
locked_investment
.user
.username
),
},
)
)

wallet.balance+=(
locked_investment.asset_amount
)

wallet.save(
update_fields=[
"balance",
"updated_at",
]
)

Transaction.objects.create(
investor=investor,
wallet=wallet,
transaction_type="investment",
direction="credit",
asset_amount=(
locked_investment.asset_amount
),
usd_value=(
locked_investment.amount_usd
),
exchange_rate=(
locked_investment.exchange_rate
),
reference=maturity_reference,
description=(
f"Return of principal for "
f"{locked_investment.plan.name} "
f"investment"
),
)

locked_investment.status="completed"

locked_investment.save(
update_fields=["status"]
)

completed_count+=1

try:
                    notify_investment_completed(
locked_investment
)
exceptExceptionasexc:
                    self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id} "
f"completed, but notification failed: "
f"{exc}"
)
)

self.stdout.write(
self.style.SUCCESS(
f"Investment "
f"#{locked_investment.id} "
f"completed and principal returned."
)
)

exceptExceptionasexc:

                self.stdout.write(
self.style.ERROR(
f"Failed to complete investment "
f"#{investment.id}: {exc}"
)
)

self.stdout.write(
self.style.SUCCESS(
f"Completed {completed_count} investment(s)."
)
)