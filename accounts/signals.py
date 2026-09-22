fromdjango.db.models.signalsimportpost_save,pre_save
fromdjango.dispatchimportreceiver
fromdjango.contrib.auth.modelsimportUser
from.modelsimportWallet
fromdecimalimportDecimal

from.modelsimport(UserProfile,Deposit,Withdrawal,Referral,)

from.notificationsimport(
notify_signup,
notify_account_verified,
notify_deposit_approved,
notify_withdrawal_approved,
notify_new_referral,
notify_referral_bonus,
)

@receiver(post_save,sender=User)
defcreate_default_wallets(sender,instance,created,**kwargs):
    ifnotcreated:
        return

currencies=[
"BTC",
"ETH",
"USDT_TRC20",
"USDT_ERC20",
]

forcurrencyincurrencies:
        Wallet.objects.get_or_create(
user=instance,
currency=currency,
)

notify_signup(instance)

@receiver(pre_save,sender=UserProfile)
defuser_profile_before_save(sender,instance,**kwargs):

    ifnotinstance.pk:
        instance._verification_changed=False
return

try:
        old_profile=UserProfile.objects.get(
pk=instance.pk
)
exceptUserProfile.DoesNotExist:
        instance._verification_changed=False
return

instance._verification_changed=(
notold_profile.kyc_verified
andinstance.kyc_verified
)


@receiver(post_save,sender=UserProfile)
defuser_profile_after_save(sender,instance,created,**kwargs):

    ifgetattr(instance,"_verification_changed",False):
        notify_account_verified(instance.user)






@receiver(pre_save,sender=Deposit)
defdeposit_before_save(sender,instance,**kwargs):

    ifnotinstance.pk:
        instance._status_changed_to_approved=False
return

try:
        old_deposit=Deposit.objects.get(
pk=instance.pk
)
exceptDeposit.DoesNotExist:
        instance._status_changed_to_approved=False
return

instance._status_changed_to_approved=(
old_deposit.status!="approved"
andinstance.status=="approved"
)


@receiver(post_save,sender=Deposit)
defdeposit_after_save(sender,instance,created,**kwargs):

    ifgetattr(instance,"_status_changed_to_approved",False):
        notify_deposit_approved(instance)






@receiver(pre_save,sender=Withdrawal)
defwithdrawal_before_save(sender,instance,**kwargs):

    ifnotinstance.pk:
        instance._status_changed_to_approved=False
return

try:
        old_withdrawal=Withdrawal.objects.get(
pk=instance.pk
)
exceptWithdrawal.DoesNotExist:
        instance._status_changed_to_approved=False
return

instance._status_changed_to_approved=(
old_withdrawal.status!="approved"
andinstance.status=="approved"
)


@receiver(post_save,sender=Withdrawal)
defwithdrawal_after_save(sender,instance,created,**kwargs):

    ifgetattr(instance,"_status_changed_to_approved",False):
        notify_withdrawal_approved(instance)






@receiver(post_save,sender=Referral)
defreferral_created(sender,instance,created,**kwargs):

    ifcreated:
        notify_new_referral(instance)






@receiver(pre_save,sender=Referral)
defreferral_before_save(sender,instance,**kwargs):

    ifnotinstance.pk:
        instance._commission_increased=False
instance._commission_difference=Decimal("0.00")
return

try:
        old_referral=Referral.objects.get(
pk=instance.pk
)
exceptReferral.DoesNotExist:
        instance._commission_increased=False
instance._commission_difference=Decimal("0.00")
return

old_amount=(
old_referral.commission_earned
orDecimal("0.00")
)

new_amount=(
instance.commission_earned
orDecimal("0.00")
)

difference=new_amount-old_amount

instance._commission_increased=difference>Decimal("0.00")
instance._commission_difference=difference


@receiver(post_save,sender=Referral)
defreferral_commission_updated(sender,instance,created,**kwargs):

    if(
notcreated
andgetattr(instance,"_commission_increased",False)
):
        notify_referral_bonus(
instance,
getattr(
instance,
"_commission_difference",
Decimal("0.00"),
),
)


