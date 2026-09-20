from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet
from decimal import Decimal

from .models import ( UserProfile, Deposit, Withdrawal, Referral, )

from .notifications import (
    notify_signup,
    notify_account_verified,
    notify_deposit_approved,
    notify_withdrawal_approved,
    notify_new_referral,
    notify_referral_bonus,
)

@receiver(post_save, sender=User)
def create_default_wallets(sender, instance, created, **kwargs):
    if not created:
        return

    currencies = [
        "BTC",
        "ETH",
        "USDT_TRC20",
        "USDT_ERC20",
    ]

    for currency in currencies:
        Wallet.objects.get_or_create(
            user=instance,
            currency=currency,
        )

    notify_signup(instance)

@receiver(pre_save, sender=UserProfile)
def user_profile_before_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._verification_changed = False
        return

    try:
        old_profile = UserProfile.objects.get(
            pk=instance.pk
        )
    except UserProfile.DoesNotExist:
        instance._verification_changed = False
        return

    instance._verification_changed = (
        not old_profile.kyc_verified
        and instance.kyc_verified
    )


@receiver(post_save, sender=UserProfile)
def user_profile_after_save(sender, instance, created, **kwargs):

    if getattr(instance, "_verification_changed", False):
        notify_account_verified(instance.user)


                                                              
                  
                                                              

@receiver(pre_save, sender=Deposit)
def deposit_before_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._status_changed_to_approved = False
        return

    try:
        old_deposit = Deposit.objects.get(
            pk=instance.pk
        )
    except Deposit.DoesNotExist:
        instance._status_changed_to_approved = False
        return

    instance._status_changed_to_approved = (
        old_deposit.status != "approved"
        and instance.status == "approved"
    )


@receiver(post_save, sender=Deposit)
def deposit_after_save(sender, instance, created, **kwargs):

    if getattr(instance, "_status_changed_to_approved", False):
        notify_deposit_approved(instance)


                                                              
                     
                                                              

@receiver(pre_save, sender=Withdrawal)
def withdrawal_before_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._status_changed_to_approved = False
        return

    try:
        old_withdrawal = Withdrawal.objects.get(
            pk=instance.pk
        )
    except Withdrawal.DoesNotExist:
        instance._status_changed_to_approved = False
        return

    instance._status_changed_to_approved = (
        old_withdrawal.status != "approved"
        and instance.status == "approved"
    )


@receiver(post_save, sender=Withdrawal)
def withdrawal_after_save(sender, instance, created, **kwargs):

    if getattr(instance, "_status_changed_to_approved", False):
        notify_withdrawal_approved(instance)


                                                              
              
                                                              

@receiver(post_save, sender=Referral)
def referral_created(sender, instance, created, **kwargs):

    if created:
        notify_new_referral(instance)


                                                              
                     
                                                              

@receiver(pre_save, sender=Referral)
def referral_before_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._commission_increased = False
        instance._commission_difference = Decimal("0.00")
        return

    try:
        old_referral = Referral.objects.get(
            pk=instance.pk
        )
    except Referral.DoesNotExist:
        instance._commission_increased = False
        instance._commission_difference = Decimal("0.00")
        return

    old_amount = (
        old_referral.commission_earned
        or Decimal("0.00")
    )

    new_amount = (
        instance.commission_earned
        or Decimal("0.00")
    )

    difference = new_amount - old_amount

    instance._commission_increased = difference > Decimal("0.00")
    instance._commission_difference = difference


@receiver(post_save, sender=Referral)
def referral_commission_updated(sender, instance, created, **kwargs):

    if (
        not created
        and getattr(instance, "_commission_increased", False)
    ):
        notify_referral_bonus(
            instance,
            getattr(
                instance,
                "_commission_difference",
                Decimal("0.00"),
            ),
        )


