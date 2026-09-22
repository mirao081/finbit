from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import Investment, Wallet
from accounts.notifications import notify_investment_completed
from core.models import Investor, Transaction


class Command(BaseCommand):

    help = (
        "Complete finite investments whose end date has elapsed, "
        "return the original principal, and notify the user."
    )

    def handle(self, *args, **options):

        now = timezone.now()

        investments = (
            Investment.objects
            .select_related("user", "plan", "wallet")
            .filter(
                status="active",
                end_date__isnull=False,
                end_date__lte=now,
            )
            .order_by("end_date")
        )

        completed_count = 0

        for investment in investments:

            try:

                with transaction.atomic():

                    locked_investment = (
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

                    if not locked_investment:
                        continue

                    if (
                        not locked_investment.wallet_id
                        or not locked_investment.asset_amount
                        or locked_investment.asset_amount <= 0
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

                    wallet = (
                        Wallet.objects
                        .select_for_update()
                        .get(
                            pk=locked_investment.wallet_id
                        )
                    )

                    maturity_reference = (
                        f"INV-MATURITY-{locked_investment.id}"
                    )

                    existing_transaction = (
                        Transaction.objects
                        .filter(
                            reference=maturity_reference
                        )
                        .first()
                    )

                    if not existing_transaction:

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

                        wallet.balance += (
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

                    locked_investment.status = "completed"

                    locked_investment.save(
                        update_fields=["status"]
                    )

                    completed_count += 1

                    try:

                        notify_investment_completed(
                            locked_investment
                        )

                    except Exception as exc:

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

            except Exception as exc:

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