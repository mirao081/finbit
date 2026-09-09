from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from .models import Notification


def create_notification(
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

    if not user:
        return None

    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    if send_email and user.email:

        def send_notification_email():
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

    return notification


                                                           
        
                                                           

def notify_signup(user):

    return create_notification(
        user=user,
        title="Welcome to Finbit",
        message=(
            "Your Finbit account has been created successfully. "
            "Welcome to Finbit. Your account is now ready to use."
        ),
        notification_type="signup",
    )


                                                           
                            
                                                           

def notify_account_verified(user):

    return create_notification(
        user=user,
        title="Account Verified",
        message=(
            "Your Finbit account has been successfully verified. "
            "You can now access the available account features."
        ),
        notification_type="verification",
    )


                                                           
                  
                                                           

def notify_deposit_approved(deposit):

    amount = (
        deposit.amount_usd
        or Decimal("0.00")
    )

    currency = (
        deposit.get_payment_method_display()
        if deposit.payment_method
        else "crypto"
    )

    plan_text = ""

    if deposit.plan:
        plan_text = (
            f" for the {deposit.plan.name} plan"
        )

    return create_notification(
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


                                                           
                    
                                                           

def notify_investment_started(investment):

    amount = (
        investment.amount_usd
        or Decimal("0.00")
    )

    plan_name = investment.plan.name

    if investment.created_at:

        start_text = investment.created_at.strftime(
            "%B %d, %Y at %I:%M %p"
        )

    else:

        start_text = "now"

    if investment.end_date:

        end_text = investment.end_date.strftime(
            "%B %d, %Y at %I:%M %p"
        )

        duration_text = (
            f"Your investment is scheduled to end on "
            f"{end_text}."
        )

    else:

        duration_text = (
            "This is a lifetime investment and has no end date."
        )

    return create_notification(
        user=investment.user,
        title="Investment Started",
        message=(
            f"Your {plan_name} investment of "
            f"${amount:,.2f} started on {start_text}. "
            f"{duration_text}"
        ),
        notification_type="investment",
    )


                                                           
                      
                                                           

def notify_investment_completed(investment):

    amount = (
        investment.amount_usd
        or Decimal("0.00")
    )

    return create_notification(
        user=investment.user,
        title="Investment Completed",
        message=(
            f"Your {investment.plan.name} investment "
            f"of ${amount:,.2f} has completed successfully."
        ),
        notification_type="investment",
    )


                                                           
                      
                                                           

def notify_withdrawal_requested(withdrawal):

    amount = (
        withdrawal.amount_usd
        or Decimal("0.00")
    )

    if withdrawal.wallet:

        currency = (
            withdrawal.wallet.get_currency_display()
        )

    else:

        currency = "crypto"

    return create_notification(
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


                                                           
                     
                                                           

def notify_withdrawal_approved(withdrawal):

    amount = (
        withdrawal.amount_usd
        or Decimal("0.00")
    )

    if withdrawal.wallet:

        currency = (
            withdrawal.wallet.get_currency_display()
        )

    else:

        currency = "crypto"

    return create_notification(
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


                                                           
              
                                                           

def notify_new_referral(referral):

    return create_notification(
        user=referral.user,
        title="New Referral",
        message=(
            f"{referral.referred_user.username} "
            "has registered on Finbit using your "
            "referral link."
        ),
        notification_type="referral",
    )


                                                           
                
                                                           

def notify_referral_bonus(
    referral,
    bonus_amount,
):

    bonus_amount = Decimal(
        bonus_amount or "0.00"
    )

    return create_notification(
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


                                                           
                       
                                                           

def notify_manual_referral_bonus(
    user,
    amount,
):

    amount = Decimal(
        amount or "0.00"
    )

    return create_notification(
        user=user,
        title="Referral Bonus Added",
        message=(
            f"A referral bonus of ${amount:,.2f} "
            "has been added to your Finbit account."
        ),
        notification_type="bonus",
    )