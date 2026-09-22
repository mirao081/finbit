
fromdatetimeimporttimedelta

fromdecimalimportDecimal,InvalidOperation,ROUND_DOWN

fromdjango.core.management.baseimportBaseCommand

fromdjango.dbimporttransaction

fromdjango.utilsimporttimezone

fromaccounts.modelsimport(
AssetPrice,
Investment,
Profit,
Wallet,
)

fromaccounts.notificationsimportnotify_profit_paid

fromcore.modelsimportInvestor,Transaction


classCommand(BaseCommand):

    help=(
"Process scheduled investment profit payouts "
"for active investments."
)

defhandle(self,*args,**options):

        now=timezone.now()

processed_count=0

investments=(
Investment.objects
.select_related(
"user",
"plan",
"wallet",
)
.filter(
status="active",
wallet__isnull=False,
amount_usd__gt=0,
)
.order_by("id")
)

forinvestmentininvestments:

            try:

                withtransaction.atomic():

                    locked_investment=(
Investment.objects
.select_for_update()
.select_related(
"user",
"plan",
"wallet",
)
.get(
pk=investment.pk
)
)

iflocked_investment.status!="active":
                        continue

ifnotlocked_investment.amount_usd:
                        continue

plan=locked_investment.plan

frequency=(
plan.frequencyor""
).lower().strip()

return_rate=(
plan.return_rateor""
).lower().strip()





if"hour"infrequency:

                        interval_seconds=(
60*60
)

elif"day"infrequency:

                        interval_seconds=(
24*60*60
)

elif"week"infrequency:

                        interval_seconds=(
7*24*60*60
)

else:

                        self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id}: "
f"unsupported frequency "
f"'{plan.frequency}'."
)
)

continue





existing_profit=(
Profit.objects
.filter(
investment=locked_investment,
payout_at__isnull=False,
)
.order_by("-payout_at")
.first()
)

ifexisting_profit:

                        next_payout_at=(
existing_profit.payout_at
+timedelta(
seconds=interval_seconds
)
)

else:

                        ifnotlocked_investment.created_at:
                            continue

next_payout_at=(
locked_investment.created_at
+timedelta(
seconds=interval_seconds
)
)









if(
notexisting_profit
andnext_payout_at<=now
):

                        next_payout_at=now





ifnext_payout_at>now:
                        continue









if(
locked_investment.end_date
andnext_payout_at
>locked_investment.end_date
):

                        continue





if"%"inreturn_rate:

                        number_text=(
return_rate
.replace("return","")
.replace("%","")
.strip()
)

try:

                            percentage=Decimal(
number_text
)

exceptInvalidOperation:

                            self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id}: "
f"invalid percentage "
f"'{plan.return_rate}'."
)
)

continue

profit_usd=(
locked_investment.amount_usd
*percentage
/Decimal("100")
)

elif"usd"inreturn_rate:

                        number_text=(
return_rate
.replace("return","")
.replace("usd","")
.strip()
)

try:

                            profit_usd=Decimal(
number_text
)

exceptInvalidOperation:

                            self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id}: "
f"invalid USD return "
f"'{plan.return_rate}'."
)
)

continue

else:

                        self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id}: "
f"unsupported return rate "
f"'{plan.return_rate}'."
)
)

continue

profit_usd=profit_usd.quantize(
Decimal("0.01"),
rounding=ROUND_DOWN,
)

ifprofit_usd<=0:
                        continue





wallet=(
Wallet.objects
.select_for_update()
.get(
pk=locked_investment.wallet_id
)
)





asset_price=(
AssetPrice.objects
.filter(
currency=wallet.currency
)
.first()
)

if(
notasset_price
ornotasset_price.usd_price
orasset_price.usd_price<=0
):

                        self.stdout.write(
self.style.WARNING(
f"Investment "
f"#{locked_investment.id}: "
f"no valid USD price for "
f"{wallet.currency}."
)
)

continue





asset_profit=(
profit_usd
/asset_price.usd_price
).quantize(
Decimal("0.000000000001"),
rounding=ROUND_DOWN,
)

ifasset_profit<=0:
                        continue






duplicate=(
Profit.objects
.filter(
investment=locked_investment,
payout_at=next_payout_at,
)
.exists()
)

ifduplicate:
                        continue





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





profit=Profit.objects.create(
user=locked_investment.user,
investment=locked_investment,
plan=plan,
amount=profit_usd,
payout_at=next_payout_at,
status="approved",
)





wallet.balance+=asset_profit

wallet.save(
update_fields=[
"balance",
"updated_at",
]
)





Transaction.objects.create(
investor=investor,
wallet=wallet,
transaction_type="profit",
direction="credit",
asset_amount=asset_profit,
usd_value=profit_usd,
exchange_rate=asset_price.usd_price,
reference=f"PROFIT-{profit.id}",
description=(
f"Profit payout from "
f"{plan.name} investment"
),
)









notify_profit_paid(profit)

processed_count+=1

self.stdout.write(
self.style.SUCCESS(
f"Investment "
f"#{locked_investment.id}: "
f"${profit_usd:,.2f} "
f"profit credited."
)
)

exceptInvestment.DoesNotExist:

                continue

exceptExceptionasexc:

                self.stdout.write(
self.style.ERROR(
f"Failed to process investment "
f"#{investment.id}: {exc}"
)
)

self.stdout.write(
self.style.SUCCESS(
f"Processed {processed_count} "
f"profit payout(s)."
)
)
