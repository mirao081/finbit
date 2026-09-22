fromdecimalimportDecimal

fromdjango.confimportsettings
fromdjango.core.mailimportsend_mail
fromdjango.dbimporttransaction

from.modelsimportNotification


defcreate_notification(
user,
title,
message,
notification_type="general",
send_email=True,
):
    """
    Creates an in-app notification and optionally sends
    an email to the user's registered email address.
    """

ifnotuser:
        returnNone

notification=Notification.objects.create(
user=user,
title=title,
message=message,
notification_type=notification_type,
)

ifsend_emailanduser.email:

        defsend_notification_email():
            send_mail(
subject=title,
message=message,
from_email=settings.DEFAULT_FROM_EMAIL,
recipient_list=[user.email],
fail_silently=True,
)

transaction.on_commit(
send_notification_email
)

returnnotification






defnotify_signup(user):

    returncreate_notification(
user=user,
title="Welcome to Finbit",
message=(
"Your Finbit account has been created successfully. "
"Welcome to Finbit. Your account is now ready to use."
),
notification_type="signup",
)






defnotify_account_verified(user):

    returncreate_notification(
user=user,
title="Account Verified",
message=(
"Your Finbit account has been successfully verified. "
"You can now access the available account features."
),
notification_type="verification",
)






defnotify_deposit_approved(deposit):

    amount=(
deposit.amount_usd
orDecimal("0.00")
)

currency=(
deposit.get_payment_method_display()
ifdeposit.payment_method
else"crypto"
)

plan_text=""

ifdeposit.plan:
        plan_text=(
f" for the {deposit.plan.name} plan"
)

returncreate_notification(
user=deposit.user,
title="Deposit Approved",
message=(
f"Your deposit of ${amount:,.2f} "
f"using {currency}{plan_text} "
"has been approved successfully and "
"credited to your account."
),
notification_type="deposit",
)






defnotify_investment_started(investment):

    amount=(
investment.amount_usd
orDecimal("0.00")
)

plan_name=investment.plan.name

ifinvestment.created_at:

        start_text=investment.created_at.strftime(
"%B %d, %Y at %I:%M %p"
)

else:

        start_text="now"

ifinvestment.end_date:

        end_text=investment.end_date.strftime(
"%B %d, %Y at %I:%M %p"
)

duration_text=(
f"Your investment is scheduled to end on "
f"{end_text}."
)

else:

        duration_text=(
"This is a lifetime investment and has no end date."
)

returncreate_notification(
user=investment.user,
title="Investment Started",
message=(
f"Your {plan_name} investment of "
f"${amount:,.2f} started on {start_text}. "
f"{duration_text}"
),
notification_type="investment",
)






defnotify_investment_completed(investment):

    amount=(
investment.amount_usd
orDecimal("0.00")
)

returncreate_notification(
user=investment.user,
title="Investment Completed",
message=(
f"Your {investment.plan.name} investment "
f"of ${amount:,.2f} has completed successfully."
),
notification_type="investment",
)






defnotify_withdrawal_requested(withdrawal):

    amount=(
withdrawal.amount_usd
orDecimal("0.00")
)

ifwithdrawal.wallet:

        currency=(
withdrawal.wallet.get_currency_display()
)

else:

        currency="crypto"

returncreate_notification(
user=withdrawal.user,
title="Withdrawal Request Received",
message=(
f"Your withdrawal request of "
f"${amount:,.2f} "
f"({withdrawal.asset_amount} {currency}) "
"has been received and is currently "
"pending approval."
),
notification_type="withdrawal",
)






defnotify_withdrawal_approved(withdrawal):

    amount=(
withdrawal.amount_usd
orDecimal("0.00")
)

ifwithdrawal.wallet:

        currency=(
withdrawal.wallet.get_currency_display()
)

else:

        currency="crypto"

returncreate_notification(
user=withdrawal.user,
title="Withdrawal Approved",
message=(
f"Your withdrawal of "
f"${amount:,.2f} "
f"({withdrawal.asset_amount} {currency}) "
"has been approved successfully."
),
notification_type="withdrawal",
)






defnotify_new_referral(referral):

    returncreate_notification(
user=referral.user,
title="New Referral",
message=(
f"{referral.referred_user.username} "
"has registered on Finbit using your "
"referral link."
),
notification_type="referral",
)






defnotify_referral_bonus(
referral,
bonus_amount,
):

    bonus_amount=Decimal(
bonus_amountor"0.00"
)

returncreate_notification(
user=referral.user,
title="Referral Bonus Earned",
message=(
f"You earned a referral bonus of "
f"${bonus_amount:,.2f} from "
f"{referral.referred_user.username}'s "
"approved deposit."
),
notification_type="bonus",
)






defnotify_manual_referral_bonus(
user,
amount,
):

    amount=Decimal(
amountor"0.00"
)

returncreate_notification(
user=user,
title="Referral Bonus Added",
message=(
f"A referral bonus of ${amount:,.2f} "
"has been added to your Finbit account."
),
notification_type="bonus",
)

defnotify_profit_paid(profit):
    amount=profit.amountorDecimal("0.00")
plan_name=profit.plan.name

returncreate_notification(
user=profit.user,
title="Investment Profit Credited",
message=(
f"A profit of ${amount:,.2f} has been credited "
f"to your {plan_name} investment."
),
notification_type="investment",
)