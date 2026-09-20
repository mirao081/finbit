
from datetime import timedelta

from decimal import Decimal, InvalidOperation, ROUND_DOWN

from django.core.management.base import BaseCommand

from django.db import transaction

from django.utils import timezone

from accounts.models import (
    AssetPrice,
    Investment,
    Profit,
    Wallet,
)

from accounts.notifications import notify_profit_paid

from core.models import Investor, Transaction


class Command(BaseCommand):

    help = (
        "Process scheduled investment profit payouts "
        "for active investments."
    )

    def handle(self, *args, **options):

        now = timezone.now()

        processed_count = 0

        investments = (
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

        for investment in investments:

            try:

                with transaction.atomic():

                    locked_investment = (
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

                    if locked_investment.status != "active":
                        continue

                    if not locked_investment.amount_usd:
                        continue

                    plan = locked_investment.plan

                    frequency = (
                        plan.frequency or ""
                    ).lower().strip()

                    return_rate = (
                        plan.return_rate or ""
                    ).lower().strip()

                    # ---------------------------------------------
                    # Determine payout interval.
                    # ---------------------------------------------

                    if "hour" in frequency:

                        interval_seconds = (
                            60 * 60
                        )

                    elif "day" in frequency:

                        interval_seconds = (
                            24 * 60 * 60
                        )

                    elif "week" in frequency:

                        interval_seconds = (
                            7 * 24 * 60 * 60
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

                    # ---------------------------------------------
                    # Find the latest existing scheduled payout.
                    # ---------------------------------------------

                    existing_profit = (
                        Profit.objects
                        .filter(
                            investment=locked_investment,
                            payout_at__isnull=False,
                        )
                        .order_by("-payout_at")
                        .first()
                    )

                    if existing_profit:

                        next_payout_at = (
                            existing_profit.payout_at
                            + timedelta(
                                seconds=interval_seconds
                            )
                        )

                    else:

                        if not locked_investment.created_at:
                            continue

                        next_payout_at = (
                            locked_investment.created_at
                            + timedelta(
                                seconds=interval_seconds
                            )
                        )

                    # ---------------------------------------------
                    # Do not create historical profits on the first
                    # run.
                    #
                    # If the first payout is already overdue,
                    # process it now.
                    # ---------------------------------------------

                    if (
                        not existing_profit
                        and next_payout_at <= now
                    ):

                        next_payout_at = now

                    # ---------------------------------------------
                    # Payout must be due.
                    # ---------------------------------------------

                    if next_payout_at > now:
                        continue

                    # ---------------------------------------------
                    # Do not pay profit after maturity.
                    #
                    # IMPORTANT:
                    # The final payout IS allowed exactly at the
                    # investment's end_date.
                    # ---------------------------------------------

                    if (
                        locked_investment.end_date
                        and next_payout_at
                        > locked_investment.end_date
                    ):

                        continue

                    # ---------------------------------------------
                    # Calculate USD profit.
                    # ---------------------------------------------

                    if "%" in return_rate:

                        number_text = (
                            return_rate
                            .replace("return", "")
                            .replace("%", "")
                            .strip()
                        )

                        try:

                            percentage = Decimal(
                                number_text
                            )

                        except InvalidOperation:

                            self.stdout.write(
                                self.style.WARNING(
                                    f"Investment "
                                    f"#{locked_investment.id}: "
                                    f"invalid percentage "
                                    f"'{plan.return_rate}'."
                                )
                            )

                            continue

                        profit_usd = (
                            locked_investment.amount_usd
                            * percentage
                            / Decimal("100")
                        )

                    elif "usd" in return_rate:

                        number_text = (
                            return_rate
                            .replace("return", "")
                            .replace("usd", "")
                            .strip()
                        )

                        try:

                            profit_usd = Decimal(
                                number_text
                            )

                        except InvalidOperation:

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

                    profit_usd = profit_usd.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_DOWN,
                    )

                    if profit_usd <= 0:
                        continue

                    # ---------------------------------------------
                    # Lock wallet.
                    # ---------------------------------------------

                    wallet = (
                        Wallet.objects
                        .select_for_update()
                        .get(
                            pk=locked_investment.wallet_id
                        )
                    )

                    # ---------------------------------------------
                    # Get current asset price.
                    # ---------------------------------------------

                    asset_price = (
                        AssetPrice.objects
                        .filter(
                            currency=wallet.currency
                        )
                        .first()
                    )

                    if (
                        not asset_price
                        or not asset_price.usd_price
                        or asset_price.usd_price <= 0
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

                    # ---------------------------------------------
                    # Convert USD profit to wallet asset.
                    # ---------------------------------------------

                    asset_profit = (
                        profit_usd
                        / asset_price.usd_price
                    ).quantize(
                        Decimal("0.000000000001"),
                        rounding=ROUND_DOWN,
                    )

                    if asset_profit <= 0:
                        continue

                    # ---------------------------------------------
                    # Prevent duplicate payout for the same
                    # scheduled payout time.
                    # ---------------------------------------------

                    duplicate = (
                        Profit.objects
                        .filter(
                            investment=locked_investment,
                            payout_at=next_payout_at,
                        )
                        .exists()
                    )

                    if duplicate:
                        continue

                    # ---------------------------------------------
                    # Create investor record if necessary.
                    # ---------------------------------------------

                    investor, _ = (
                        Investor.objects
                        .get_or_create(
                            user=locked_investment.user,
                            defaults={
                                "name": (
                                    locked_investment
                                    .user
                                    .username
                                ),
                            },
                        )
                    )

                    # ---------------------------------------------
                    # Create profit record.
                    # ---------------------------------------------

                    profit = Profit.objects.create(
                        user=locked_investment.user,
                        investment=locked_investment,
                        plan=plan,
                        amount=profit_usd,
                        payout_at=next_payout_at,
                        status="approved",
                    )

                    # ---------------------------------------------
                    # Credit user's wallet.
                    # ---------------------------------------------

                    wallet.balance += asset_profit

                    wallet.save(
                        update_fields=[
                            "balance",
                            "updated_at",
                        ]
                    )

                    # ---------------------------------------------
                    # Record profit transaction.
                    # ---------------------------------------------

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

                    # ---------------------------------------------
                    # Send profit notification.
                    #
                    # This creates:
                    # 1 in-app notification
                    # 1 email
                    # ---------------------------------------------

                    notify_profit_paid(profit)

                    processed_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Investment "
                            f"#{locked_investment.id}: "
                            f"${profit_usd:,.2f} "
                            f"profit credited."
                        )
                    )

            except Investment.DoesNotExist:

                continue

            except Exception as exc:

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
