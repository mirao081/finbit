importpyotp
fromdecimalimportDecimal,InvalidOperation
fromdjango.dbimporttransaction
fromdjango.core.validatorsimportvalidate_email
fromdjango.core.exceptionsimportValidationError
fromioimportBytesIO
importbase64
importcsv
importjson
importsecrets
importstring
importrandom
fromdatetimeimporttimedelta
fromdjango.core.mailimportsend_mail
fromdjango.utilsimporttimezone
fromdjango.contrib.auth.hashersimportcheck_password,make_password
importrequests
fromdjango.core.cacheimportcache
importpyotp
importqrcode
importtime
fromdjangoimportforms
fromdjango.contribimportmessages
fromdjango.contrib.authimportlogin,logout
fromdjango.contrib.auth.formsimportUserCreationForm
fromdjango.contrib.auth.modelsimportUser
fromdjango.contrib.auth.viewsimportLoginView
fromdjango.contrib.auth.decoratorsimportlogin_required
fromdjango.contrib.sessions.modelsimportSession
fromdjango.core.paginatorimportPaginator
fromdjango.dbimporttransaction
fromdjango.db.modelsimportSum,Count
fromdjango.httpimportJsonResponse,HttpResponse
fromdjango.shortcutsimportrender,redirect,get_object_or_404
fromdjango.utils.safestringimportmark_safe
fromdjango.views.decorators.httpimportrequire_POST
fromdjango.confimportsettings
from.utilsimport(
generate_recovery_codes,
verify_recovery_code,
)
fromcore.modelsimport(
SiteSettings,
MenuItem,
Transaction,
Investor,
InvestmentPlan,
ProfitCalculatorSection,
)

from.modelsimport(
DashboardMenu,
UserProfile,
KYCSubmission,
QuickAction,
Wallet,
CompanyWallet,
Deposit,
Withdrawal,
Investment,
Profit,
Bonus,
Referral,
SupportPage,
ProfilePage,
InvestmentHowItWorks,
InvestmentPageContent,
InvestmentFAQ,
SecurityCenterContent,
TwoFactorAuth,
RecoveryOTP,
RecoveryCode,
Announcement,
AnnouncementRead,
AnnouncementReply,
AssetPrice,
Notification,
Trade,
TradeGasPayment,
)

from.formsimport(
KYCForm,
WalletForm,
DepositForm,
WithdrawalForm,
ProfilePictureForm,
SettingsForm,
SignupForm,
LoginForm
)
from.notificationsimport(
notify_signup,
notify_investment_started,
notify_withdrawal_requested,
notify_new_referral,
)





classUserLoginView(LoginView):
    template_name="accounts/login.html"
redirect_authenticated_user=False

authentication_form=LoginForm

MAX_LOGIN_ATTEMPTS=5
LOGIN_BLOCK_TIME=5*7*24*60*60

defget_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)

context["site_settings"]=SiteSettings.objects.first()

context["menu_items"]=MenuItem.objects.filter(
is_active=True
)

context["recaptcha_site_key"]=(
settings.RECAPTCHA_SITE_KEY
)

returncontext

defget_login_key(self):
        username=self.request.POST.get(
"username",
"",
).strip().lower()

ip_address=self.request.META.get(
"REMOTE_ADDR",
"unknown",
)

returnf"login_attempts:{ip_address}:{username}"

defis_rate_limited(self):
        key=self.get_login_key()

attempts=cache.get(
key,
0,
)

returnattempts>=self.MAX_LOGIN_ATTEMPTS

defrecord_failed_attempt(self):
        key=self.get_login_key()

attempts=cache.get(
key,
0,
)

attempts+=1

cache.set(
key,
attempts,
self.LOGIN_BLOCK_TIME,
)

defclear_failed_attempts(self):
        cache.delete(
self.get_login_key()
)

defform_invalid(self,form):
        recaptcha_response=self.request.POST.get(
"g-recaptcha-response",
"",
)

ifnotrecaptcha_response:
            messages.error(
self.request,
"Please complete the reCAPTCHA verification.",
)

returnsuper().form_invalid(form)

defform_valid(self,form):

        ifself.is_rate_limited():

            messages.error(
self.request,
"Too many failed login attempts. "
"Please try again later.",
)

returnsuper().form_invalid(form)

recaptcha_response=self.request.POST.get(
"g-recaptcha-response",
"",
)

ifnotrecaptcha_response:

            messages.error(
self.request,
"Please complete the reCAPTCHA verification.",
)

returnsuper().form_invalid(form)

try:

            recaptcha_result=requests.post(
"https://www.google.com/recaptcha/api/siteverify",
data={
"secret":settings.RECAPTCHA_SECRET_KEY,
"response":recaptcha_response,
"remoteip":self.request.META.get(
"REMOTE_ADDR"
),
},
timeout=10,
)

recaptcha_result.raise_for_status()

recaptcha_data=(
recaptcha_result.json()
)

except(
requests.RequestException,
ValueError,
):

            messages.error(
self.request,
"reCAPTCHA verification failed. "
"Please try again.",
)

returnsuper().form_invalid(form)

ifnotrecaptcha_data.get("success"):

            messages.error(
self.request,
"Please complete the reCAPTCHA verification correctly.",
)

returnsuper().form_invalid(form)

user=form.get_user()

ifuserisNone:

            self.record_failed_attempt()

messages.error(
self.request,
"Invalid username/email or password.",
)

returnsuper().form_invalid(form)

ifnotuser.is_active:

            self.record_failed_attempt()

messages.error(
self.request,
"This account is inactive.",
)

returnsuper().form_invalid(form)

self.clear_failed_attempts()

two_factor,_=TwoFactorAuth.objects.get_or_create(
user=user
)

if(
two_factor.is_enabled
andtwo_factor.secret_key
):

            importtime

self.request.session[
"pending_2fa_user_id"
]=user.id

self.request.session[
"pending_2fa_started_at"
]=time.time()

self.request.session[
"pending_2fa_authenticated_at"
]=self.request.session.get(
"_auth_user_id"
)

self.request.session[
"pending_2fa_login_type"
]="user"

self.request.session.modified=True

returnredirect(
"two_factor_login"
)

returnsuper().form_valid(form)

defget_success_url(self):

        user=self.request.user

ifuser.is_superuseroruser.is_staff:

            returnredirect(
"admin_dashboard"
).url

returnredirect(
"dashboard"
).url


defsignup(request):

    referrer_username=(
request.GET.get("ref")
orrequest.session.get("referrer_username")
)

referrer=None

ifreferrer_username:
        try:
            referrer=User.objects.get(
username=referrer_username
)

exceptUser.DoesNotExist:
            try:
                referrer=UserProfile.objects.get(
referral_code=referrer_username
).user

exceptUserProfile.DoesNotExist:
                request.session.pop(
"referrer_username",
None,
)

ifreferrer:
            request.session["referrer_username"]=(
referrer.username
)

ifrequest.method=="POST":

        form=SignupForm(request.POST)

recaptcha_response=request.POST.get(
"g-recaptcha-response",
"",
)

ifnotrecaptcha_response:

            messages.error(
request,
"Please complete the reCAPTCHA verification.",
)

else:

            try:

                recaptcha_result=requests.post(
"https://www.google.com/recaptcha/api/siteverify",
data={
"secret":settings.RECAPTCHA_SECRET_KEY,
"response":recaptcha_response,
"remoteip":request.META.get(
"REMOTE_ADDR"
),
},
timeout=10,
)

recaptcha_result.raise_for_status()

recaptcha_data=(
recaptcha_result.json()
)

except(
requests.RequestException,
ValueError,
):

                messages.error(
request,
"reCAPTCHA verification failed. Please try again.",
)

else:

                ifnotrecaptcha_data.get("success"):

                    messages.error(
request,
"Please complete the reCAPTCHA verification correctly.",
)

elifform.is_valid():

                    user=form.save()




if(
referrer
andreferrer.pk!=user.pk
):

                        referral,created=(
Referral.objects.get_or_create(
user=referrer,
referred_user=user,
)
)

ifcreated:

                            UserProfile.objects.filter(
user=user
).update(
referrer=referrer
)




request.session.pop(
"referrer_username",
None,
)

login(
request,
user,
)

returnredirect("home")

else:

        form=SignupForm()

returnrender(
request,
"accounts/signup.html",
{
"form":form,
"recaptcha_site_key":(
settings.RECAPTCHA_SITE_KEY
),
},
)

defuser_logout(request):
    logout(request)
returnredirect("login")



@login_required
defdashboard(request):

    site_settings=SiteSettings.objects.first()

menu_items=MenuItem.objects.filter(
is_active=True
)

quick_actions=QuickAction.objects.all()

menus=DashboardMenu.objects.all()

profile,_=UserProfile.objects.get_or_create(
user=request.user
)





wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)





deposit_total=(
Deposit.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
).quantize(Decimal("0.01"))





withdrawal_total=(
Withdrawal.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
).quantize(Decimal("0.01"))








wallet_balance=Decimal("0.00")

forwalletinwallets:

        available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0.00"):
            available_asset=Decimal("0.00")

asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
            continue

exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
            continue

wallet_usd_value=(
available_asset*exchange_rate
)

wallet_balance+=wallet_usd_value

wallet_balance=wallet_balance.quantize(
Decimal("0.01")
)







available_balance=wallet_balance





active_investments=(
Investment.objects
.filter(
user=request.user,
status="active",
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
).quantize(Decimal("0.01"))





profit_total=(
Profit.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount")
)["total"]
orDecimal("0.00")
).quantize(Decimal("0.01"))





bonus_total=(
Bonus.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount")
)["total"]
orDecimal("0.00")
).quantize(Decimal("0.01"))





total_earned=(
profit_total+bonus_total
).quantize(Decimal("0.01"))










total_balance=(
wallet_balance
+active_investments
+profit_total
+bonus_total
).quantize(Decimal("0.01"))





referral_link=request.build_absolute_uri(
f"/signup/?ref={profile.referral_codeorrequest.user.username}"
)

referral_count=Referral.objects.filter(
user=request.user
).count()







automatic_referral_bonus=(
Referral.objects
.filter(user=request.user)
.aggregate(
total=Sum("commission_earned")
)["total"]
orDecimal("0.00")
)





manual_referral_bonus=(
Bonus.objects
.filter(
user=request.user,
status="approved",
bonus_type="manual",
description__iexact="Referral bonus",
)
.aggregate(
total=Sum("amount")
)["total"]
orDecimal("0.00")
)





referral_bonus=(
automatic_referral_bonus
+manual_referral_bonus
).quantize(
Decimal("0.01")
)





submission=(
KYCSubmission.objects
.filter(user=request.user)
.last()
)

form=KYCForm()





investor,_=Investor.objects.get_or_create(
user=request.user,
defaults={
"name":request.user.username,
},
)





recent_transactions=[]





deposits=(
Deposit.objects
.filter(user=request.user)
.select_related("plan")
.order_by("-created_at")
)

fordepositindeposits:

        recent_transactions.append({
"date":deposit.created_at,
"type":"Deposit",
"amount":deposit.amount_usd,
"asset":deposit.get_payment_method_display(),
"asset_code":deposit.payment_method,
"status":deposit.status,
"asset_amount":(
deposit.received_asset_amount
ordeposit.asset_amount
),
"plan":(
deposit.plan.name
ifdeposit.plan
elseNone
),
})





withdrawals=(
Withdrawal.objects
.filter(user=request.user)
.select_related("wallet")
.order_by("-created_at")
)

forwithdrawalinwithdrawals:

        wallet=withdrawal.wallet

recent_transactions.append({
"date":withdrawal.created_at,
"type":"Withdrawal",
"amount":withdrawal.amount_usd,
"asset":(
wallet.get_currency_display()
ifwallet
else"—"
),
"asset_code":(
wallet.currency
ifwallet
else"—"
),
"status":withdrawal.status,
"asset_amount":withdrawal.asset_amount,
"plan":None,
})





investments=(
Investment.objects
.filter(user=request.user)
.select_related("plan","wallet")
.order_by("-created_at")
)

forinvestmentininvestments:

        wallet=investment.wallet

recent_transactions.append({
"date":investment.created_at,
"type":"Investment",
"amount":investment.amount_usd,
"asset":(
wallet.get_currency_display()
ifwallet
else"—"
),
"asset_code":(
wallet.currency
ifwallet
else"—"
),
"status":investment.status,
"asset_amount":investment.asset_amount,
"plan":(
investment.plan.name
ifinvestment.plan
elseNone
),
})





recent_transactions.sort(
key=lambdaitem:item["date"]ortimezone.now(),
reverse=True,
)





transactions=recent_transactions[:5]





latest_announcement=(
Announcement.objects
.filter(is_active=True)
.order_by("-created_at")
.first()
)

unread=(
latest_announcement
andnotAnnouncementRead.objects.filter(
user=request.user,
announcement=latest_announcement,
).exists()
)





unread_announcements_count=(
AnnouncementReply.objects
.filter(
user=request.user,
is_read_by_user=False,
)
.count()
)





notifications=(
Notification.objects
.filter(user=request.user)
.order_by("-created_at")[:10]
)

unread_notifications_count=(
Notification.objects
.filter(
user=request.user,
is_read=False,
)
.count()
)





context={





"site_settings":site_settings,
"menu_items":menu_items,
"menus":menus,
"profile":profile,
"submission":submission,
"form":form,
"investor":investor,
"transactions":transactions,
"quick_actions":quick_actions,





"latest_announcement":latest_announcement,

"unread_announcement":unread,

"unread_announcements_count":(
unread_announcements_count
),





"notifications":notifications,

"unread_notifications_count":(
unread_notifications_count
),





"deposit_total":deposit_total,

"withdrawal_total":withdrawal_total,


"wallet_balance":wallet_balance,


"available_balance":available_balance,


"active_investments":active_investments,


"profit_total":profit_total,

"bonus_total":bonus_total,

"total_earned":total_earned,


"total_balance":total_balance,





"wallets":wallets,





"referral_link":referral_link,

"referral_count":referral_count,

"referral_bonus":referral_bonus,
}

returnrender(
request,
"accounts/dashboard.html",
context,
)

@login_required
defnotifications(request):
    notification_queryset=Notification.objects.filter(
user=request.user
).order_by("-created_at")

unread_notifications_count=notification_queryset.filter(
is_read=False
).count()

paginator=Paginator(notification_queryset,10)

page_number=request.GET.get("page")
notification_page=paginator.get_page(page_number)

returnrender(
request,
"accounts/notifications.html",
{
"notifications":notification_page,
"unread_notifications_count":unread_notifications_count,
},
)

@login_required
@require_POST
defmark_notification_read(
request,
notification_id,
):

    notification=get_object_or_404(
Notification,
id=notification_id,
user=request.user,
)

notification.is_read=True

notification.save(
update_fields=["is_read"]
)

returnredirect(
"notifications"
)


@login_required
@require_POST
defmark_all_notifications_read(request):

    Notification.objects.filter(
user=request.user,
is_read=False,
).update(
is_read=True
)

returnredirect(
"notifications"
)

@login_required
defwallets(request):

    site_settings=SiteSettings.objects.first()

menus=DashboardMenu.objects.all()





user_wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)








forwalletinuser_wallets:





        available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0"):
            available_asset=Decimal("0")

wallet.available_asset=available_asset





asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

if(
asset_price
andasset_price.usd_price
andasset_price.usd_price.is_finite()
andasset_price.usd_price>Decimal("0")
):
            wallet.available_usd=(
available_asset
*asset_price.usd_price
).quantize(
Decimal("0.01")
)
else:
            wallet.available_usd=Decimal("0.00")





wallet.qr_base64=None

ifwallet.address:

            qr=qrcode.make(wallet.address)

buffer=BytesIO()

qr.save(
buffer,
format="PNG",
)

wallet.qr_base64=base64.b64encode(
buffer.getvalue()
).decode()





transactions=(
wallet.transactions
.all()
.order_by("-date")
)

paginator=Paginator(
transactions,
4
)

page_parameter=f"tx_page_{wallet.id}"

wallet.transaction_page=paginator.get_page(
request.GET.get(page_parameter)
)

wallet.transaction_page_parameter=page_parameter





ifrequest.method=="POST":

        form=WalletForm(request.POST)

ifform.is_valid():

            currency=form.cleaned_data["currency"]
address=form.cleaned_data["address"]

wallet=(
Wallet.objects
.filter(
user=request.user,
currency=currency,
)
.first()
)

ifwallet:

                wallet.address=address

wallet.save(
update_fields=[
"address",
]
)

else:

                wallet=form.save(commit=False)

wallet.user=request.user

wallet.save()

returnredirect("wallets")

else:

        form=WalletForm()





returnrender(
request,
"accounts/wallets.html",
{
"wallets":user_wallets,
"form":form,
"menus":menus,
"site_settings":site_settings,
},
)

@login_required
defedit_wallet(request,wallet_id):
    wallet=get_object_or_404(
Wallet,
id=wallet_id,
user=request.user,
)

ifrequest.method=="POST":
        form=WalletForm(
request.POST,
instance=wallet,
)

ifform.is_valid():
            form.save()
returnredirect("wallets")
else:
        form=WalletForm(
instance=wallet
)

returnrender(
request,
"accounts/edit_wallet.html",
{
"form":form,
"wallet":wallet,
},
)


@login_required
defdelete_wallet(request,wallet_id):
    wallet=get_object_or_404(
Wallet,
id=wallet_id,
user=request.user,
)

ifrequest.method=="POST":
        wallet.delete()
returnredirect("wallets")

returnredirect(
"confirm_delete_wallet",
wallet_id=wallet.id,
)


@login_required
defconfirm_delete_wallet(request,wallet_id):
    wallet=get_object_or_404(
Wallet,
id=wallet_id,
user=request.user,
)

ifrequest.method=="POST":
        wallet.delete()
returnredirect("wallets")

returnrender(
request,
"accounts/confirm_delete.html",
{
"wallet":wallet,
},
)


@login_required
defdeposit(request):
    site_settings=SiteSettings.objects.first()
menu_items=MenuItem.objects.filter(is_active=True)
menus=DashboardMenu.objects.all()
plans=InvestmentPlan.objects.all()

deposits_qs=(
Deposit.objects
.filter(user=request.user)
.select_related("plan")
.order_by("-created_at")
)

paginator=Paginator(deposits_qs,5)
page_number=request.GET.get("page")
deposits_page=paginator.get_page(page_number)

ifrequest.method=="POST":
        form=DepositForm(
request.POST,
request.FILES,
)

ifform.is_valid():
            deposit=form.save(commit=False)

deposit.user=request.user
deposit.status="pending"
deposit.credited_to_wallet=False

deposit.save()

returnredirect(
"deposit_invoice",
deposit_id=deposit.id,
)

else:
        form=DepositForm()

returnrender(
request,
"accounts/deposit.html",
{
"site_settings":site_settings,
"menu_items":menu_items,
"menus":menus,
"form":form,
"plans":plans,
"deposits":deposits_page,
},
)


@login_required
defdeposit_invoice(request,deposit_id):
    deposit=get_object_or_404(
Deposit,
id=deposit_id,
user=request.user,
)

company_wallet=(
CompanyWallet.objects
.filter(
currency=deposit.payment_method
)
.first()
)

returnrender(
request,
"accounts/deposit_invoice.html",
{
"deposit":deposit,
"company_wallet":company_wallet,
},
)

@login_required
defdeposit_invoice(request,deposit_id):
    deposit=get_object_or_404(
Deposit,
id=deposit_id,
user=request.user,
)

company_wallet=(
CompanyWallet.objects
.filter(
currency=deposit.payment_method
)
.first()
)

returnrender(
request,
"accounts/deposit_invoice.html",
{
"deposit":deposit,
"company_wallet":company_wallet,
},
)


@login_required
defstart_investment(request):

    site_settings=SiteSettings.objects.first()

menu_items=MenuItem.objects.filter(
is_active=True
)

menus=DashboardMenu.objects.all()

plans=InvestmentPlan.objects.all()

investment_faqs=InvestmentFAQ.objects.filter(
is_active=True
)





wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)











wallet_balance=Decimal("0.00")

user_wallets=list(wallets)

asset_prices={
price.currency:price.usd_price
forpriceinAssetPrice.objects.filter(
currency__in=[
wallet.currency
forwalletinuser_wallets
]
)
}

forwalletinuser_wallets:

        rate=asset_prices.get(
wallet.currency
)

if(
rateisNone
ornotrate.is_finite()
orrate<=Decimal("0")
):
            continue

available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0"):
            available_asset=Decimal("0")

wallet_balance+=(
available_asset*rate
)

wallet_balance=wallet_balance.quantize(
Decimal("0.01")
)

balance=wallet_balance





ifrequest.method=="POST":





        plan_id=request.POST.get("plan")
amount_value=request.POST.get("amount")
wallet_currency=request.POST.get(
"wallet_currency"
)





try:

            plan=InvestmentPlan.objects.get(
id=plan_id
)

except(
InvestmentPlan.DoesNotExist,
TypeError,
ValueError,
):

            messages.error(
request,
"The selected investment plan does not exist.",
)

returnredirect(
"start_investment"
)





try:

            amount_usd=Decimal(
amount_value
)

except(
TypeError,
ValueError,
ArithmeticError,
InvalidOperation,
):

            messages.error(
request,
"Please enter a valid investment amount.",
)

returnredirect(
"start_investment"
)

ifnotamount_usd.is_finite():

            messages.error(
request,
"Please enter a valid investment amount.",
)

returnredirect(
"start_investment"
)

ifamount_usd<=Decimal("0.00"):

            messages.error(
request,
"Investment amount must be greater than zero.",
)

returnredirect(
"start_investment"
)





amount_usd=amount_usd.quantize(
Decimal("0.01")
)





ifamount_usd<plan.minimum_investment:

            messages.error(
request,
(
f"Minimum investment for {plan.name} "
f"is ${plan.minimum_investment}."
),
)

returnredirect(
"start_investment"
)





if(
plan.maximum_investmentisnotNone
andamount_usd>plan.maximum_investment
):

            messages.error(
request,
(
f"Maximum investment for {plan.name} "
f"is ${plan.maximum_investment}."
),
)

returnredirect(
"start_investment"
)





ifnotwallet_currency:

            messages.error(
request,
"Please select a wallet to invest from.",
)

returnredirect(
"start_investment"
)





allowed_wallets={
"BTC",
"ETH",
"USDT_TRC20",
"USDT_ERC20",
}

ifwallet_currencynotinallowed_wallets:

            messages.error(
request,
"The selected wallet is not valid.",
)

returnredirect(
"start_investment"
)





withtransaction.atomic():





            wallet=(
Wallet.objects
.select_for_update()
.filter(
user=request.user,
currency=wallet_currency,
)
.first()
)

ifnotwallet:

                messages.error(
request,
"The selected wallet could not be found.",
)

returnredirect(
"start_investment"
)





asset_price=(
AssetPrice.objects
.filter(
currency=wallet.currency
)
.first()
)

ifnotasset_price:

                messages.error(
request,
(
"No USD exchange rate has been "
f"configured for "
f"{wallet.get_currency_display()}."
),
)

returnredirect(
"start_investment"
)

exchange_rate=asset_price.usd_price





if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):

                messages.error(
request,
"The selected wallet exchange rate is invalid.",
)

returnredirect(
"start_investment"
)








asset_amount=(
amount_usd/exchange_rate
)

asset_amount=asset_amount.quantize(
Decimal("0.000000000001")
)

ifasset_amount<=Decimal("0"):

                messages.error(
request,
"The calculated asset amount is invalid.",
)

returnredirect(
"start_investment"
)





available_balance=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_balance<Decimal("0"):

                available_balance=Decimal("0")





ifasset_amount>available_balance:

                available_usd=(
available_balance
*exchange_rate
).quantize(
Decimal("0.01")
)

messages.error(
request,
(
f"Insufficient available "
f"{wallet.get_currency_display()} "
f"balance. You need approximately "
f"{asset_amount} "
f"{wallet.currency}, worth "
f"${amount_usd}, but only "
f"${available_usd} is available."
),
)

returnredirect(
"start_investment"
)





wallet.balance-=asset_amount

wallet.save(
update_fields=[
"balance",
"updated_at",
]
)










investment=Investment.objects.create(
user=request.user,
plan=plan,
amount_usd=amount_usd,
wallet=wallet,
asset_amount=asset_amount,
exchange_rate=exchange_rate,
status="active",
)





investor,_=(
Investor.objects
.get_or_create(
user=request.user,
defaults={
"name":request.user.username,
},
)
)





Transaction.objects.create(
investor=investor,
wallet=wallet,
transaction_type="investment",
direction="debit",
asset_amount=asset_amount,
usd_value=amount_usd,
exchange_rate=exchange_rate,
reference=f"INV-{investment.id}",
description=(
f"Investment in "
f"{plan.name} using "
f"{wallet.get_currency_display()}"
),
)








try:

            notify_investment_started(
investment
)

exceptException:



            pass





messages.success(
request,
(
f"You have successfully invested "
f"${amount_usd} in {plan.name} "
f"using {wallet.get_currency_display()}."
),
)

returnredirect(
"dashboard"
)





returnrender(
request,
"accounts/start_investment.html",
{
"site_settings":site_settings,
"menu_items":menu_items,
"menus":menus,
"plans":plans,
"wallets":wallets,
"balance":balance,
"investment_faqs":investment_faqs,
},
)

@login_required
defwithdraw(request):
    site_settings=SiteSettings.objects.first()
menu_items=MenuItem.objects.filter(is_active=True)
menus=DashboardMenu.objects.all()


user_profile,profile_created=UserProfile.objects.get_or_create(
user=request.user
)

user_wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)

withdrawals_qs=(
Withdrawal.objects
.filter(user=request.user)
.select_related("wallet")
.order_by("-created_at")
)

paginator=Paginator(withdrawals_qs,5)

withdrawals=paginator.get_page(
request.GET.get("page")
)

ifrequest.method=="POST":
        form=WithdrawalForm(request.POST)

ifform.is_valid():
            wallet_currency=form.cleaned_data["wallet_currency"]
amount_usd=form.cleaned_data["amount_usd"]
destination_wallet=form.cleaned_data["destination_wallet"]

wallet=(
Wallet.objects
.filter(
user=request.user,
currency=wallet_currency
)
.first()
)

ifnotwallet:
                form.add_error(
"wallet_currency",
"A wallet for the selected asset was not found."
)

elifnotwallet.address:
                form.add_error(
"wallet_currency",
"Please add a wallet address for this asset before withdrawing."
)

else:
                asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
                    form.add_error(
"wallet_currency",
f"No USD exchange rate has been configured for "
f"{wallet.get_currency_display()}."
)

else:
                    exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
                        form.add_error(
"wallet_currency",
"The exchange rate for the selected asset is invalid."
)

else:
                        asset_amount=(
amount_usd/exchange_rate
).quantize(
Decimal("0.000000000001")
)

available_balance=(
wallet.balance-wallet.reserved_balance
)

ifavailable_balance<Decimal("0.00"):
                            available_balance=Decimal("0.00")

ifasset_amount>available_balance:
                            available_usd=(
available_balance*exchange_rate
).quantize(
Decimal("0.01")
)

form.add_error(
"amount_usd",
(
f"Insufficient available "
f"{wallet.get_currency_display()} balance. "
f"You need approximately {asset_amount} "
f"{wallet.currency}, worth ${amount_usd}, "
f"but only ${available_usd} is available."
)
)

else:
                            request.session["withdrawal_confirmation"]={
"wallet_currency":wallet.currency,
"amount_usd":str(amount_usd),
"asset_amount":str(asset_amount),
"exchange_rate":str(exchange_rate),
"wallet_id":wallet.id,
"destination_wallet":destination_wallet,
}

request.session.modified=True

returnredirect("withdraw_invoice")

else:
        form=WithdrawalForm()

total_wallet_balance=Decimal("0.00")

forwalletinuser_wallets:
        asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
            continue

exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
            continue

available_asset=(
wallet.balance-wallet.reserved_balance
)

ifavailable_asset<Decimal("0.00"):
            available_asset=Decimal("0.00")

total_wallet_balance+=(
available_asset*exchange_rate
)

total_wallet_balance=total_wallet_balance.quantize(
Decimal("0.01")
)

context={
"site_settings":site_settings,
"menu_items":menu_items,
"menus":menus,
"user_profile":user_profile,
"user_wallets":user_wallets,
"wallet_balance":total_wallet_balance,
"available_balance":total_wallet_balance,
"withdrawals":withdrawals,
"withdrawals_page":withdrawals,
"form":form,
}

returnrender(
request,
"accounts/withdraw.html",
context
)




@login_required
defwithdraw_invoice(request):

    confirmation=request.session.get(
"withdrawal_confirmation"
)

ifnotconfirmation:
        messages.error(
request,
"Your withdrawal confirmation has expired or is no longer available."
)
returnredirect("withdraw")

wallet_currency=confirmation.get(
"wallet_currency"
)

amount_usd_string=confirmation.get(
"amount_usd"
)

wallet_id=confirmation.get(
"wallet_id"
)





try:
        amount_usd=Decimal(
amount_usd_string
)
except(
TypeError,
ValueError,
ArithmeticError,
):
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifnotamount_usd.is_finite():
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifamount_usd<=Decimal("0.00"):
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifamount_usd<Decimal("6.00"):
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Minimum withdrawal is $6."
)

returnredirect("withdraw")





wallet=(
Wallet.objects
.filter(
id=wallet_id,
user=request.user,
currency=wallet_currency,
)
.first()
)

ifnotwallet:
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The selected wallet could not be found."
)

returnredirect("withdraw")





ifnotwallet.address:
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The wallet address is no longer available."
)

returnredirect("withdraw")





asset_price=(
AssetPrice.objects
.filter(
currency=wallet.currency
)
.first()
)

ifnotasset_price:
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
(
f"No USD exchange rate has been configured "
f"for {wallet.get_currency_display()}."
)
)

returnredirect("withdraw")

exchange_rate=asset_price.usd_price





if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The selected asset exchange rate is invalid."
)

returnredirect("withdraw")







asset_amount=(
amount_usd/exchange_rate
)

asset_amount=asset_amount.quantize(
Decimal("0.000000000001")
)

ifasset_amount<=Decimal("0"):
        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The calculated withdrawal amount is invalid."
)

returnredirect("withdraw")





available_balance=(
wallet.balance-
wallet.reserved_balance
)

ifavailable_balance<Decimal("0.00"):
        available_balance=Decimal("0.00")





ifasset_amount>available_balance:

        available_usd=(
available_balance*exchange_rate
).quantize(
Decimal("0.01")
)

request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
(
f"Insufficient available "
f"{wallet.get_currency_display()} balance. "
f"You requested ${amount_usd}, which requires "
f"{asset_amount} {wallet.currency}. "
f"Your available balance is "
f"{available_balance} {wallet.currency}, "
f"worth approximately ${available_usd}."
)
)

returnredirect("withdraw")





available_balance_usd=(
available_balance*exchange_rate
).quantize(
Decimal("0.01")
)





context={

"site_settings":(
SiteSettings.objects.first()
),

"menu_items":(
MenuItem.objects
.filter(is_active=True)
),

"menus":(
DashboardMenu.objects.all()
),

"wallet":wallet,

"asset":wallet_currency,

"amount":amount_usd,

"amount_usd":amount_usd,

"asset_amount":asset_amount,

"exchange_rate":exchange_rate,

"available_balance":available_balance,

"available_balance_usd":available_balance_usd,

}

returnrender(
request,
"accounts/withdraw_invoice.html",
context,
)

@login_required
@require_POST
defconfirm_withdrawal(request):

    confirmation=request.session.get(
"withdrawal_confirmation"
)

ifnotconfirmation:
        messages.error(
request,
"Your withdrawal confirmation has expired. Please start again."
)
returnredirect("withdraw")

wallet_currency=confirmation.get(
"wallet_currency"
)

amount_usd_string=confirmation.get(
"amount_usd"
)

wallet_id=confirmation.get(
"wallet_id"
)

destination_wallet=confirmation.get(
"destination_wallet"
)





try:
        amount_usd=Decimal(
amount_usd_string
)
except(
TypeError,
ValueError,
ArithmeticError,
):

        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifnotamount_usd.is_finite():

        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifamount_usd<=Decimal("0.00"):

        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Invalid withdrawal amount."
)

returnredirect("withdraw")

ifamount_usd<Decimal("6.00"):

        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"Minimum withdrawal is $6."
)

returnredirect("withdraw")





ifnotdestination_wallet:

        request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"A destination wallet address is required."
)

returnredirect("withdraw")





withtransaction.atomic():





        wallet=(
Wallet.objects
.select_for_update()
.filter(
id=wallet_id,
user=request.user,
currency=wallet_currency,
)
.first()
)

ifnotwallet:

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The selected wallet could not be found."
)

returnredirect("withdraw")





ifnotwallet.address:

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The wallet address is no longer available."
)

returnredirect("withdraw")





asset_price=(
AssetPrice.objects
.filter(
currency=wallet.currency
)
.first()
)

ifnotasset_price:

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
(
f"No USD exchange rate has been configured "
f"for {wallet.get_currency_display()}."
)
)

returnredirect("withdraw")

exchange_rate=asset_price.usd_price





if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The selected asset exchange rate is invalid."
)

returnredirect("withdraw")





asset_amount=(
amount_usd/exchange_rate
)

asset_amount=asset_amount.quantize(
Decimal("0.000000000001")
)

ifasset_amount<=Decimal("0"):

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
"The calculated withdrawal amount is invalid."
)

returnredirect("withdraw")





available_balance=(
wallet.balance-
wallet.reserved_balance
)

ifavailable_balance<Decimal("0.00"):

            available_balance=Decimal("0.00")










ifasset_amount>available_balance:

            request.session.pop(
"withdrawal_confirmation",
None
)

messages.error(
request,
(
"Your available balance has changed. "
"There is no longer enough "
f"{wallet.get_currency_display()} "
"to complete this withdrawal."
)
)

returnredirect("withdraw")





wallet.reserved_balance+=asset_amount

wallet.save(
update_fields=[
"reserved_balance"
]
)





withdrawal=Withdrawal.objects.create(
user=request.user,
wallet=wallet,
amount_usd=amount_usd,
asset_amount=asset_amount,
exchange_rate=exchange_rate,
destination_wallet=destination_wallet,
status="pending",
)





request.session.pop(
"withdrawal_confirmation",
None
)

messages.success(
request,
(
"Withdrawal request submitted successfully "
"and is awaiting approval."
)
)

returnredirect(
"withdrawal_confirmation_success",
withdrawal_id=withdrawal.id,
)


@login_required
defwithdrawal_confirmation_success(request,withdrawal_id):

    withdrawal=(
Withdrawal.objects
.filter(
id=withdrawal_id,
user=request.user,
)
.first()
)

ifnotwithdrawal:
        messages.error(
request,
"The withdrawal request could not be found."
)

returnredirect("withdraw")

returnrender(
request,
"accounts/withdrawal_confirmation_success.html",
{
"site_settings":SiteSettings.objects.first(),
"menu_items":MenuItem.objects.filter(
is_active=True
),
"menus":DashboardMenu.objects.all(),
"withdrawal":withdrawal,
},
)

@login_required
deflive_trade_withdrawal(request,trade_id):

    trade=get_object_or_404(
Trade.objects.select_related(
"deposit",
"plan",
),
id=trade_id,
user=request.user,
)

iftrade.result!="win":
        messages.error(
request,
"Only winning Live Trading trades can be withdrawn.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

ifnottrade.payout_released:
        messages.error(
request,
"This trade payout has not been released yet.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

ifhasattr(trade,"withdrawal"):
        messages.warning(
request,
"This Live Trading payout has already been submitted for withdrawal.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

payout_transaction=(
Transaction.objects
.filter(
investor__user=request.user,
transaction_type="profit",
direction="credit",
reference=f"TRADE-PAYOUT-{trade.id}",
)
.select_related("wallet")
.first()
)

ifnotpayout_transaction:
        messages.error(
request,
"The released Live Trading payout could not be found.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

ifnotpayout_transaction.wallet:
        messages.error(
request,
"The payout wallet could not be found.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

wallet=payout_transaction.wallet

available_balance=wallet.available_balance

if(
notpayout_transaction.asset_amount
orpayout_transaction.asset_amount<=0
):
        messages.error(
request,
"The Live Trading payout amount is invalid.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

ifpayout_transaction.asset_amount>available_balance:
        messages.error(
request,
"The Live Trading payout is no longer available in the wallet.",
)
returnredirect(
"trade_result",
trade_id=trade.id,
)

ifrequest.method=="POST":

        destination_wallet=request.POST.get(
"destination_wallet",
"",
).strip()

ifnotdestination_wallet:
            messages.error(
request,
"Enter the destination wallet address.",
)
returnrender(
request,
"accounts/live_trade_withdrawal.html",
{
"trade":trade,
"transaction":payout_transaction,
"wallet":wallet,
},
)

withdrawal=Withdrawal.objects.create(
user=request.user,
wallet=wallet,
trade=trade,
amount_usd=payout_transaction.usd_value,
asset_amount=payout_transaction.asset_amount,
exchange_rate=payout_transaction.exchange_rate,
destination_wallet=destination_wallet,
status="pending",
source="live_trade",
)

wallet.reserved_balance+=payout_transaction.asset_amount

wallet.save(
update_fields=[
"reserved_balance",
"updated_at",
],
)

messages.success(
request,
"Your Live Trading withdrawal request has been submitted for admin approval.",
)

returnredirect(
"withdrawal_confirmation_success",
withdrawal_id=withdrawal.id,
)

returnrender(
request,
"accounts/live_trade_withdrawal.html",
{
"trade":trade,
"transaction":payout_transaction,
"wallet":wallet,
},
)

@login_required
deftransactions(request):

    deposits=(
Deposit.objects
.filter(user=request.user)
.select_related("plan")
.order_by("-created_at")
)

withdrawals=(
Withdrawal.objects
.filter(user=request.user)
.select_related("wallet")
.order_by("-created_at")
)

investments=(
Investment.objects
.filter(user=request.user)
.select_related("plan","wallet")
.order_by("-created_at")
)

transaction_list=[]


fordepositindeposits:

        transaction_list.append({
"date":deposit.created_at,
"type":"Deposit",
"asset":deposit.get_payment_method_display(),
"asset_code":deposit.payment_method,
"amount":deposit.amount_usd,
"asset_amount":(
deposit.received_asset_amount
ordeposit.asset_amount
),
"status":deposit.status,
"plan":(
deposit.plan.name
ifdeposit.plan
elseNone
),
})


forwithdrawalinwithdrawals:

        wallet=withdrawal.wallet

transaction_list.append({
"date":withdrawal.created_at,
"type":"Withdrawal",
"asset":(
wallet.get_currency_display()
ifwallet
else"—"
),
"asset_code":(
wallet.currency
ifwallet
else"—"
),
"amount":withdrawal.amount_usd,
"asset_amount":withdrawal.asset_amount,
"status":withdrawal.status,
"plan":None,
})


forinvestmentininvestments:

        wallet=investment.wallet

transaction_list.append({
"date":investment.created_at,
"type":"Investment",
"asset":(
wallet.get_currency_display()
ifwallet
else"—"
),
"asset_code":(
wallet.currency
ifwallet
else"—"
),
"amount":investment.amount_usd,
"asset_amount":investment.asset_amount,
"status":investment.status,
"plan":(
investment.plan.name
ifinvestment.plan
elseNone
),
})


transaction_list.sort(
key=lambdaitem:item["date"],
reverse=True,
)


paginator=Paginator(
transaction_list,
5,
)

page_number=request.GET.get("page")

page_obj=paginator.get_page(page_number)

returnrender(
request,
"accounts/transactions.html",
{
"page_obj":page_obj,
},
)

@login_required
defprofit_history(request):
    profits_qs=(
Profit.objects
.filter(user=request.user)
.order_by("created_at")
)

labels=[
p.created_at.strftime("%b %d")
forpinprofits_qs
]

data_points=[
float(p.amount)
forpinprofits_qs
]

paginator=Paginator(
profits_qs.order_by("-created_at"),
5,
)

page_number=request.GET.get("page")
profits_page=paginator.get_page(
page_number
)

total_profit=(
profits_qs.aggregate(
Sum("amount")
)["amount__sum"]
or0
)

active_investments=(
Investment.objects
.filter(
user=request.user,
status="active",
)
.count()
)

average_roi=0

ifactive_investments>0:
        average_roi=round(
total_profit/active_investments,
2,
)

section=ProfitCalculatorSection.objects.first()

returnrender(
request,
"accounts/profit_history.html",
{
"profits":profits_page,
"total_profit":total_profit,
"active_investments":active_investments,
"average_roi":average_roi,
"section":section,
"profit_labels":mark_safe(
json.dumps(labels)
),
"profit_data":mark_safe(
json.dumps(data_points)
),
},
)


@login_required
defreferrals(request):
    referral_link=request.build_absolute_uri(
f"/signup/?ref={request.user.username}"
)





referrals_qs=(
Referral.objects
.filter(user=request.user)
.select_related("referred_user")
)

total_referrals=referrals_qs.count()








total_earnings=(
referrals_qs.aggregate(
total=Sum("commission_earned")
)["total"]
orDecimal("0.00")
)

total_earnings=total_earnings.quantize(
Decimal("0.01")
)





paginator=Paginator(
referrals_qs.order_by("-created_at"),
10,
)

page_number=request.GET.get("page")

referred_page=paginator.get_page(
page_number
)





chart_data={
"labels":[
"Total Referrals",
"Total Earnings",
],
"values":[
total_referrals,
float(total_earnings),
],
}





returnrender(
request,
"accounts/referrals.html",
{
"referral_link":referral_link,
"total_referrals":total_referrals,
"total_earnings":total_earnings,
"referred_users":referred_page,
"chart_data":mark_safe(
json.dumps(chart_data)
),
},
)

@login_required
defmarkets(request):
    returnrender(
request,
"accounts/markets.html"
)


@login_required
defsupport(request):
    support_page=SupportPage.objects.first()
menus=DashboardMenu.objects.all()

returnrender(
request,
"accounts/support.html",
{
"support_page":support_page,
"menus":menus,
},
)


@login_required
defprofile(request):
    profile_page=ProfilePage.objects.first()

user_profile,created=(
UserProfile.objects.get_or_create(
user=request.user
)
)





ifrequest.method=="POST":
        form=ProfilePictureForm(
request.POST,
request.FILES,
instance=user_profile,
)

ifform.is_valid():
            form.save()

messages.success(
request,
"Profile picture updated successfully.",
)

returnredirect("profile")
else:
        form=ProfilePictureForm(
instance=user_profile
)





plans=InvestmentPlan.objects.all()





pending_deposits=(
Deposit.objects
.filter(
user=request.user,
status="pending",
)
.order_by("-created_at")
)

approved_deposits=(
Deposit.objects
.filter(
user=request.user,
status="approved",
)
.order_by("-created_at")
)





investments=(
Investment.objects
.filter(
user=request.user,
status="active",
)
.select_related("plan","wallet")
.order_by("-created_at")
)





wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)











wallet_balance=Decimal("0.00")

forwalletinwallets:

        available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0"):
            available_asset=Decimal("0")

asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
            continue

exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
            continue

wallet_balance+=(
available_asset*exchange_rate
)

wallet_balance=wallet_balance.quantize(
Decimal("0.01")
)





profit_total=(
Profit.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount")
)["total"]
orDecimal("0.00")
)

profit_total=profit_total.quantize(
Decimal("0.01")
)





bonus_total=(
Bonus.objects
.filter(
user=request.user,
status="approved",
)
.aggregate(
total=Sum("amount")
)["total"]
orDecimal("0.00")
)

bonus_total=bonus_total.quantize(
Decimal("0.01")
)

referral_earnings=(
Referral.objects
.filter(user=request.user)
.aggregate(
total=Sum("commission_earned")
)["total"]
orDecimal("0.00")
)

referral_earnings=referral_earnings.quantize(
Decimal("0.01")
)







investment_total=(
investments
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
)

investment_total=investment_total.quantize(
Decimal("0.01")
)












total_balance=wallet_balance





btc_wallet=(
Wallet.objects
.filter(
user=request.user,
currency="BTC",
)
.first()
)

eth_wallet=(
Wallet.objects
.filter(
user=request.user,
currency="ETH",
)
.first()
)

usdt_erc20_wallet=(
Wallet.objects
.filter(
user=request.user,
currency="USDT_ERC20",
)
.first()
)

usdt_trc20_wallet=(
Wallet.objects
.filter(
user=request.user,
currency="USDT_TRC20",
)
.first()
)





returnrender(
request,
"accounts/profile.html",
{
"profile_page":profile_page,
"user_profile":user_profile,

"plans":plans,

"investments":investments,
"investment_total":investment_total,

"pending_deposits":pending_deposits,
"approved_deposits":approved_deposits,

"wallets":wallets,

"btc_wallet":btc_wallet,
"eth_wallet":eth_wallet,
"usdt_erc20_wallet":usdt_erc20_wallet,
"usdt_trc20_wallet":usdt_trc20_wallet,

"form":form,

"wallet_balance":wallet_balance,
"profit_total":profit_total,
"bonus_total":bonus_total,

"total_balance":total_balance,
"referral_earnings":referral_earnings,
},
)


@login_required
defsecurity_center(request):
    activities=[]

context={
"activities":activities,
"content":{
"hero_title":"Security Center",
"hero_subtitle":"Protect your Finbit account with advanced security features.",
"twofa_title":"Two-Factor Authentication",
"twofa_text":"Add an extra layer of protection.",
"compliance_title":"Compliance & Verification",
"compliance_text":"Verify your identity for higher limits.",
"activity_title":"Device & Login Activity",
"activity_text":"Monitor recent sign-ins.",
"controls_title":"Account Controls",
"controls_text":"Manage your password.",
"alerts_title":"Security Alerts",
"alerts_text":"Important security notifications.",
},
}

returnrender(
request,
"accounts/security_center.html",
context,
)


@login_required
deftwo_factor_setup(request):
    two_factor,created=(
TwoFactorAuth.objects.get_or_create(
user=request.user
)
)




iftwo_factor.is_enabled:

        ifrequest.method=="POST":

            action=request.POST.get(
"action",
""
).strip()




ifaction=="generate_recovery_codes":

                recovery_codes=generate_recovery_codes(
request.user
)

returnrender(
request,
"accounts/two_factor_setup.html",
{
"two_factor_enabled":True,
"recovery_codes":recovery_codes,
"recovery_codes_generated":True,
},
)




ifaction=="disable_2fa":

                code=request.POST.get(
"disable_code",
""
).strip()

if(
notcode.isdigit()
orlen(code)!=6
):

                    messages.error(
request,
"Please enter the current 6-digit authenticator code."
)

returnrender(
request,
"accounts/two_factor_setup.html",
{
"two_factor_enabled":True,
},
)

totp=pyotp.TOTP(
two_factor.secret_key
)

ifnottotp.verify(
code,
valid_window=1,
):

                    messages.error(
request,
"The authenticator code is incorrect. 2FA has not been disabled."
)

returnrender(
request,
"accounts/two_factor_setup.html",
{
"two_factor_enabled":True,
},
)


two_factor.is_enabled=False

two_factor.save(
update_fields=["is_enabled"]
)


RecoveryCode.objects.filter(
user=request.user
).delete()

messages.success(
request,
"Two-Factor Authentication has been disabled successfully."
)

returnredirect(
"security_center"
)

returnrender(
request,
"accounts/two_factor_setup.html",
{
"two_factor_enabled":True,
},
)





ifnottwo_factor.secret_key:

        two_factor.secret_key=pyotp.random_base32()

two_factor.save(
update_fields=["secret_key"]
)

totp=pyotp.TOTP(
two_factor.secret_key
)

provisioning_uri=totp.provisioning_uri(
name=(
request.user.email
orrequest.user.username
),
issuer_name="Finbit",
)

qr=qrcode.make(
provisioning_uri
)

buffer=BytesIO()

qr.save(
buffer,
format="PNG",
)

qr_code=base64.b64encode(
buffer.getvalue()
).decode()

ifrequest.method=="POST":

        code=request.POST.get(
"code",
""
).strip()

if(
notcode.isdigit()
orlen(code)!=6
):

            messages.error(
request,
"Please enter the 6-digit verification code."
)

eliftotp.verify(
code,
valid_window=1,
):

            two_factor.is_enabled=True

two_factor.save(
update_fields=["is_enabled"]
)

messages.success(
request,
"Two-Factor Authentication has been enabled successfully."
)

returnredirect(
"security_center"
)

else:

            messages.error(
request,
"The verification code is incorrect. Please try again."
)

returnrender(
request,
"accounts/two_factor_setup.html",
{
"qr_code":qr_code,
"secret_key":two_factor.secret_key,
"two_factor_enabled":False,
},
)


deftwo_factor_login(request):
    importtime

pending_user_id=request.session.get(
"pending_2fa_user_id"
)

pending_started_at=request.session.get(
"pending_2fa_started_at"
)

ifnotpending_user_idornotpending_started_at:
        messages.error(
request,
"Your two-factor authentication session has expired. Please log in again.",
)

returnredirect("login")

iftime.time()-pending_started_at>10*60:
        request.session.pop(
"pending_2fa_user_id",
None,
)

request.session.pop(
"pending_2fa_started_at",
None,
)

request.session.pop(
"pending_2fa_authenticated_at",
None,
)

request.session.pop(
"pending_2fa_login_type",
None,
)

request.session.modified=True

messages.error(
request,
"Your two-factor authentication session has expired. Please log in again.",
)

returnredirect("login")

user=User.objects.filter(
id=pending_user_id,
is_active=True,
).first()

ifnotuser:
        request.session.pop(
"pending_2fa_user_id",
None,
)

request.session.pop(
"pending_2fa_started_at",
None,
)

request.session.pop(
"pending_2fa_authenticated_at",
None,
)

request.session.pop(
"pending_2fa_login_type",
None,
)

request.session.modified=True

messages.error(
request,
"Unable to verify your account. Please log in again.",
)

returnredirect("login")

two_factor=(
TwoFactorAuth.objects
.filter(
user=user,
is_enabled=True,
)
.first()
)

ifnottwo_factorornottwo_factor.secret_key:
        request.session.pop(
"pending_2fa_user_id",
None,
)

request.session.pop(
"pending_2fa_started_at",
None,
)

request.session.pop(
"pending_2fa_authenticated_at",
None,
)

request.session.pop(
"pending_2fa_login_type",
None,
)

request.session.modified=True

messages.error(
request,
"Two-factor authentication is not properly configured for this account.",
)

returnredirect("login")

rate_limit_key=(
f"2fa_attempts:"
f"{user.id}:"
f"{request.META.get('REMOTE_ADDR','unknown')}"
)

attempts=cache.get(
rate_limit_key,
0,
)

ifattempts>=5:
        messages.error(
request,
"Too many verification attempts. Please try again later.",
)

returnrender(
request,
"accounts/two_factor_login.html",
)

ifrequest.method=="POST":

        code=request.POST.get(
"code",
"",
).strip()

ifnotcode:
            messages.error(
request,
"Please enter your authenticator code or recovery code.",
)

returnrender(
request,
"accounts/two_factor_login.html",
)

verified=False





ifcode.isdigit()andlen(code)==6:

            try:
                totp=pyotp.TOTP(
two_factor.secret_key
)

verified=totp.verify(
code,
valid_window=1,
)

except(
ValueError,
TypeError,
):
                verified=False





ifnotverified:

            verified=verify_recovery_code(
user,
code,
)





ifnotverified:

            attempts+=1

cache.set(
rate_limit_key,
attempts,
5*60,
)

messages.error(
request,
"The authenticator or recovery code is invalid.",
)

returnrender(
request,
"accounts/two_factor_login.html",
)





cache.delete(
rate_limit_key
)

login_type=request.session.get(
"pending_2fa_login_type",
"user",
)

request.session.pop(
"pending_2fa_user_id",
None,
)

request.session.pop(
"pending_2fa_started_at",
None,
)

request.session.pop(
"pending_2fa_authenticated_at",
None,
)

request.session.pop(
"pending_2fa_login_type",
None,
)

request.session.modified=True

login(
request,
user,
backend="django.contrib.auth.backends.ModelBackend",
)

if(
login_type=="admin"
and(
user.is_staff
oruser.is_superuser
)
):
            returnredirect(
"admin_dashboard"
)

ifuser.is_stafforuser.is_superuser:
            returnredirect(
"admin_dashboard"
)

returnredirect(
"dashboard"
)

returnrender(
request,
"accounts/two_factor_login.html",
)


@login_required
deflogin_activity(request):
    returnrender(
request,
"accounts/login_activity.html",
)


@login_required
@require_POST
defrevoke_sessions(request):
    current=request.session.session_key

forsessioninSession.objects.all():
        data=session.get_decoded()

ifstr(
data.get("_auth_user_id")
)==str(request.user.id):
            if(
session.session_key
!=current
):
                session.delete()

messages.success(
request,
"Other active sessions have been revoked.",
)

returnredirect(
"security_center"
)


@login_required
defaccount_settings(request):
    ifrequest.method=="POST":
        form=SettingsForm(
request.user,
request.POST,
)

ifform.is_valid():
            form.save()

messages.success(
request,
"Settings updated successfully.",
)

returnredirect(
"settings"
)
else:
        form=SettingsForm(
request.user
)

returnrender(
request,
"accounts/settings.html",
{
"form":form
},
)


@login_required
defdelete_account(request):
    ifrequest.method=="POST":
        user=request.user

logout(request)
user.delete()

returnredirect(
"account_deleted"
)

returnrender(
request,
"accounts/delete_account.html"
)


defaccount_deleted(request):
    returnrender(
request,
"accounts/account_deleted.html"
)


@login_required
defannouncements(request):
    announcements_list=(
Announcement.objects
.filter(is_active=True)
.order_by("-created_at")
)

paginator=Paginator(
announcements_list,
5,
)

page_number=request.GET.get("page")
announcements=paginator.get_page(
page_number
)

unread_announcements_count=(
AnnouncementReply.objects
.filter(
user=request.user,
is_read_by_user=False,
)
.count()
)

ifrequest.method=="POST":
        ann_id=request.POST.get(
"announcement_id"
)

message=(
request.POST.get(
"message",
"",
)
.strip()
)

ifann_idandmessage:
            ann=get_object_or_404(
Announcement,
id=ann_id,
is_active=True,
)

AnnouncementReply.objects.create(
announcement=ann,
user=request.user,
message=message,
is_read_by_admin=False,
is_read_by_user=True,
)

returnredirect(
"announcements"
)

AnnouncementReply.objects.filter(
user=request.user,
is_read_by_user=False,
).update(
is_read_by_user=True
)

returnrender(
request,
"accounts/announcements.html",
{
"announcements":announcements,
"unread_announcements_count":unread_announcements_count,
},
)


@login_required
defkyc_verification(request):
    submission=(
KYCSubmission.objects
.filter(user=request.user)
.last()
)

ifrequest.method=="POST":
        form=KYCForm(
request.POST,
request.FILES,
)

ifform.is_valid():
            kyc=form.save(
commit=False
)

kyc.user=request.user
kyc.save()

returnredirect(
"dashboard"
)
else:
        form=KYCForm()

returnrender(
request,
"accounts/kyc_verification.html",
{
"submission":submission,
"form":form,
},
)


@login_required
defperformance_data(request):
    wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)

wallet_balance=Decimal("0.00")

forwalletinwallets:
        available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0"):
            available_asset=Decimal("0")

asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
            continue

exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
            continue

wallet_balance+=(
available_asset*exchange_rate
)

wallet_balance=wallet_balance.quantize(
Decimal("0.01")
)

investment_balance=(
Investment.objects
.filter(
user=request.user,
status="active",
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
)

investment_balance=investment_balance.quantize(
Decimal("0.01")
)

data={
"labels":[
"Total Balance",
"Investment Balance",
],
"values":[
float(wallet_balance),
float(investment_balance),
],
}

returnJsonResponse(data)



defgenerate_recovery_otp():
    """
    Generate a cryptographically secure 6-digit OTP.
    """
returnf"{secrets.randbelow(1_000_000):06d}"


defsend_recovery_email_otp(user,email,otp):
    """
    Send recovery OTP through Django's configured email backend.

    During development, the console email backend will print
    the email and OTP in the terminal.
    """

send_mail(
subject="Finbit Recovery Verification Code",
message=(
f"Hello {user.username},\n\n"
f"Your Finbit recovery verification code is:\n\n"
f"{otp}\n\n"
f"This code expires in 10 minutes.\n\n"
f"If you did not request this verification, "
f"please secure your account immediately.\n\n"
f"Finbit Security"
),
from_email=settings.DEFAULT_FROM_EMAIL,
recipient_list=[email],
fail_silently=False,
)


defsend_recovery_sms_otp(phone,otp):
    """
    Development SMS sender.

    This does NOT send a real SMS yet.
    It prints the OTP to the development terminal.

    A real SMS provider can replace this later.
    """

print("\n"+"="*60)
print("FINBIT DEVELOPMENT SMS")
print("="*60)
print(f"To: {phone}")
print(f"Your Finbit recovery verification code is: {otp}")
print("This code expires in 10 minutes.")
print("="*60+"\n")


defcreate_recovery_otp(
user,
channel,
purpose="recovery_change",
):
    """
    Create and securely store a recovery OTP.
    """

otp=generate_recovery_otp()


code_hash=make_password(otp)



RecoveryOTP.objects.filter(
user=user,
channel=channel,
purpose=purpose,
is_verified=False,
).delete()

recovery_otp=RecoveryOTP.objects.create(
user=user,
channel=channel,
purpose=purpose,
code_hash=code_hash,
expires_at=timezone.now()+timedelta(
minutes=10
),
)

returnrecovery_otp,otp


defcan_send_recovery_otp(request,channel,purpose):
    """
    Prevent repeated OTP requests for the same verification
    purpose and channel.

    Different recovery stages are allowed to send immediately.
    """

key=(
f"recovery_otp_send:"
f"{request.user.id}:"
f"{channel}:"
f"{purpose}"
)

ifcache.get(key):
        returnFalse

cache.set(
key,
True,
60
)

returnTrue


defsend_recovery_verification_codes(request):
    """
    Generate and send both recovery verification codes.
    """

user=request.user

profile,_=UserProfile.objects.get_or_create(
user=user
)

sent_channels=[]




ifprofile.recovery_email:

        ifcan_send_recovery_otp(
request,
"email",
"recovery_authorization",
):
            _,email_otp=create_recovery_otp(
user=user,
channel="email",
purpose="recovery_authorization",
)

send_recovery_email_otp(
user=user,
email=profile.recovery_email,
otp=email_otp,
)

sent_channels.append("email")






ifprofile.recovery_phone:

        ifcan_send_recovery_otp(
request,
"sms",
"recovery_authorization",
):
            _,sms_otp=create_recovery_otp(
user=user,
channel="sms",
purpose="recovery_authorization",
)

send_recovery_sms_otp(
phone=profile.recovery_phone,
otp=sms_otp,
)

sent_channels.append("sms")


returnsent_channels


@login_required
defupdate_recovery(request):

    profile,_=UserProfile.objects.get_or_create(
user=request.user
)





defclear_recovery_session():

        session_keys=[
"pending_recovery_user_id",
"pending_recovery_email",
"pending_recovery_phone",

"recovery_old_email",
"recovery_old_phone",

"recovery_verification_stage",

"recovery_old_email_verified",
"recovery_old_sms_verified",

"recovery_email_verified",
"recovery_sms_verified",

"recovery_authenticator_verified",
"recovery_authenticator_first",

"recovery_started_at",
]

forkeyinsession_keys:
            request.session.pop(key,None)

request.session.modified=True

defrecovery_session_is_valid():

        pending_user_id=request.session.get(
"pending_recovery_user_id"
)

ifnotpending_user_id:
            returnFalse

ifstr(pending_user_id)!=str(request.user.id):
            returnFalse

recovery_started_at=request.session.get(
"recovery_started_at"
)

ifnotrecovery_started_at:
            returnFalse

try:
            recovery_started_at=float(
recovery_started_at
)
except(TypeError,ValueError):
            returnFalse

iftime.time()-recovery_started_at>10*60:
            returnFalse

returnTrue

defrender_stage(stage):

        returnrender(
request,
"accounts/update_recovery.html",
{
"verification_stage":stage
}
)

defsecurity_failure(message):

        clear_recovery_session()

messages.error(
request,
message
)

returnredirect(
"update_recovery"
)





defcomplete_recovery_update():

        ifnotrecovery_session_is_valid():
            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

pending_email=request.session.get(
"pending_recovery_email"
)

pending_phone=request.session.get(
"pending_recovery_phone"
)

ifnotpending_emailornotpending_phone:
            returnsecurity_failure(
"Recovery information is incomplete. Please start again."
)





ifnotrequest.session.get(
"recovery_email_verified"
):
            returnsecurity_failure(
"Recovery email verification was not completed."
)

ifnotrequest.session.get(
"recovery_sms_verified"
):
            returnsecurity_failure(
"Recovery phone verification was not completed."
)





old_email=request.session.get(
"recovery_old_email"
)

old_phone=request.session.get(
"recovery_old_phone"
)

if(
old_email
andnotrequest.session.get(
"recovery_old_email_verified"
)
):
            returnsecurity_failure(
"Existing recovery email verification was not completed."
)

if(
old_phone
andnotrequest.session.get(
"recovery_old_sms_verified"
)
):
            returnsecurity_failure(
"Existing recovery phone verification was not completed."
)





two_factor=(
TwoFactorAuth.objects
.filter(
user=request.user,
is_enabled=True,
)
.first()
)

iftwo_factorandtwo_factor.secret_key:

            ifnotrequest.session.get(
"recovery_authenticator_verified"
):
                returnsecurity_failure(
"Authenticator verification was not completed."
)





withtransaction.atomic():

            profile.recovery_email=pending_email
profile.recovery_phone=pending_phone

profile.save(
update_fields=[
"recovery_email",
"recovery_phone",
]
)




RecoveryOTP.objects.filter(
user=request.user,
purpose__in=[
"recovery_authorization",
"recovery_change",
],
).delete()





clear_recovery_session()

messages.success(
request,
"Recovery information updated successfully."
)

returnredirect(
"security_center"
)





recovery_started_at=request.session.get(
"recovery_started_at"
)

ifrecovery_started_at:

        try:
            recovery_started_at=float(
recovery_started_at
)

except(TypeError,ValueError):

            clear_recovery_session()

messages.error(
request,
"Your recovery verification session has expired. Please start again."
)

returnredirect(
"update_recovery"
)

iftime.time()-recovery_started_at>10*60:

            clear_recovery_session()

messages.error(
request,
"Your recovery verification session has expired. Please start again."
)

returnredirect(
"update_recovery"
)





if(
request.method=="POST"
andrequest.POST.get("action")
=="verify_old_email_otp"
):

        ifnotrecovery_session_is_valid():

            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

code=request.POST.get(
"otp_code",
""
).strip()

ifnotcode.isdigit()orlen(code)!=6:

            messages.error(
request,
"Please enter the 6-digit email verification code."
)

returnrender_stage(
"old_email"
)

recovery_otp=(
RecoveryOTP.objects
.filter(
user=request.user,
channel="email",
purpose="recovery_authorization",
is_verified=False,
)
.order_by("-created_at")
.first()
)

ifnotrecovery_otp:

            returnsecurity_failure(
"No active verification code was found. Please start again."
)

iftimezone.now()>recovery_otp.expires_at:

            recovery_otp.delete()

returnsecurity_failure(
"Your email verification code has expired. Please start again."
)

ifrecovery_otp.attempts>=5:

            recovery_otp.delete()

returnsecurity_failure(
"Too many incorrect email verification attempts. Please start again later."
)

ifnotcheck_password(
code,
recovery_otp.code_hash
):

            recovery_otp.attempts+=1

recovery_otp.save(
update_fields=["attempts"]
)

messages.error(
request,
"The email verification code is incorrect."
)

returnrender_stage(
"old_email"
)





recovery_otp.is_verified=True

recovery_otp.save(
update_fields=["is_verified"]
)

request.session[
"recovery_old_email_verified"
]=True





old_phone=request.session.get(
"recovery_old_phone"
)

ifold_phone:

            ifnotcan_send_recovery_otp(
request,
"sms",
"recovery_authorization",
):

                messages.error(
request,
"Please wait before requesting another SMS verification code."
)

returnrender_stage(
"old_sms"
)

_,sms_otp=create_recovery_otp(
user=request.user,
channel="sms",
purpose="recovery_authorization",
)

send_recovery_sms_otp(
phone=old_phone,
otp=sms_otp,
)

request.session[
"recovery_verification_stage"
]="old_sms"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your existing recovery phone."
)

returnrender_stage(
"old_sms"
)






new_email=request.session.get(
"pending_recovery_email"
)

ifnotnew_email:

            returnsecurity_failure(
"Recovery information is incomplete. Please start again."
)

ifnotcan_send_recovery_otp(
request,
"email",
"recovery_change",
):

            messages.error(
request,
"Please wait before requesting another email verification code."
)

returnrender_stage(
"new_email"
)

_,email_otp=create_recovery_otp(
user=request.user,
channel="email",
purpose="recovery_change",
)

send_recovery_email_otp(
user=request.user,
email=new_email,
otp=email_otp,
)

request.session[
"recovery_verification_stage"
]="new_email"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your new recovery email."
)

returnrender_stage(
"new_email"
)





if(
request.method=="POST"
andrequest.POST.get("action")
=="verify_old_sms_otp"
):

        ifnotrecovery_session_is_valid():

            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

code=request.POST.get(
"otp_code",
""
).strip()

ifnotcode.isdigit()orlen(code)!=6:

            messages.error(
request,
"Please enter the 6-digit SMS verification code."
)

returnrender_stage(
"old_sms"
)

recovery_otp=(
RecoveryOTP.objects
.filter(
user=request.user,
channel="sms",
purpose="recovery_authorization",
is_verified=False,
)
.order_by("-created_at")
.first()
)

ifnotrecovery_otp:

            returnsecurity_failure(
"No active SMS verification code was found. Please start again."
)

iftimezone.now()>recovery_otp.expires_at:

            recovery_otp.delete()

returnsecurity_failure(
"Your SMS verification code has expired. Please start again."
)

ifrecovery_otp.attempts>=5:

            recovery_otp.delete()

returnsecurity_failure(
"Too many incorrect SMS verification attempts. Please start again later."
)

ifnotcheck_password(
code,
recovery_otp.code_hash
):

            recovery_otp.attempts+=1

recovery_otp.save(
update_fields=["attempts"]
)

messages.error(
request,
"The SMS verification code is incorrect."
)

returnrender_stage(
"old_sms"
)





recovery_otp.is_verified=True

recovery_otp.save(
update_fields=["is_verified"]
)

request.session[
"recovery_old_sms_verified"
]=True





new_email=request.session.get(
"pending_recovery_email"
)

ifnotnew_email:

            returnsecurity_failure(
"Recovery information is incomplete. Please start again."
)

ifnotcan_send_recovery_otp(
request,
"email",
"recovery_change",
):

            messages.error(
request,
"Please wait before requesting another email verification code."
)

returnrender_stage(
"new_email"
)

_,email_otp=create_recovery_otp(
user=request.user,
channel="email",
purpose="recovery_change",
)

send_recovery_email_otp(
user=request.user,
email=new_email,
otp=email_otp,
)

request.session[
"recovery_verification_stage"
]="new_email"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your new recovery email."
)

returnrender_stage(
"new_email"
)





if(
request.method=="POST"
andrequest.POST.get("action")
=="verify_new_email_otp"
):

        ifnotrecovery_session_is_valid():

            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

code=request.POST.get(
"otp_code",
""
).strip()

ifnotcode.isdigit()orlen(code)!=6:

            messages.error(
request,
"Please enter the 6-digit email verification code."
)

returnrender_stage(
"new_email"
)

recovery_otp=(
RecoveryOTP.objects
.filter(
user=request.user,
channel="email",
purpose="recovery_change",
is_verified=False,
)
.order_by("-created_at")
.first()
)

ifnotrecovery_otp:

            returnsecurity_failure(
"No active email verification code was found. Please start again."
)

iftimezone.now()>recovery_otp.expires_at:

            recovery_otp.delete()

returnsecurity_failure(
"Your email verification code has expired. Please start again."
)

ifrecovery_otp.attempts>=5:

            recovery_otp.delete()

returnsecurity_failure(
"Too many incorrect email verification attempts. Please start again later."
)

ifnotcheck_password(
code,
recovery_otp.code_hash
):

            recovery_otp.attempts+=1

recovery_otp.save(
update_fields=["attempts"]
)

messages.error(
request,
"The email verification code is incorrect."
)

returnrender_stage(
"new_email"
)





recovery_otp.is_verified=True

recovery_otp.save(
update_fields=["is_verified"]
)

request.session[
"recovery_email_verified"
]=True





new_phone=request.session.get(
"pending_recovery_phone"
)

ifnotnew_phone:

            returnsecurity_failure(
"Recovery information is incomplete. Please start again."
)

ifnotcan_send_recovery_otp(
request,
"sms",
"recovery_change",
):

            messages.error(
request,
"Please wait before requesting another SMS verification code."
)

returnrender_stage(
"new_sms"
)

_,sms_otp=create_recovery_otp(
user=request.user,
channel="sms",
purpose="recovery_change",
)

send_recovery_sms_otp(
phone=new_phone,
otp=sms_otp,
)

request.session[
"recovery_verification_stage"
]="new_sms"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your new recovery phone."
)

returnrender_stage(
"new_sms"
)





if(
request.method=="POST"
andrequest.POST.get("action")
=="verify_new_sms_otp"
):

        ifnotrecovery_session_is_valid():

            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

code=request.POST.get(
"otp_code",
""
).strip()

ifnotcode.isdigit()orlen(code)!=6:

            messages.error(
request,
"Please enter the 6-digit SMS verification code."
)

returnrender_stage(
"new_sms"
)

recovery_otp=(
RecoveryOTP.objects
.filter(
user=request.user,
channel="sms",
purpose="recovery_change",
is_verified=False,
)
.order_by("-created_at")
.first()
)

ifnotrecovery_otp:

            returnsecurity_failure(
"No active SMS verification code was found. Please start again."
)

iftimezone.now()>recovery_otp.expires_at:

            recovery_otp.delete()

returnsecurity_failure(
"Your SMS verification code has expired. Please start again."
)

ifrecovery_otp.attempts>=5:

            recovery_otp.delete()

returnsecurity_failure(
"Too many incorrect SMS verification attempts. Please start again later."
)

ifnotcheck_password(
code,
recovery_otp.code_hash
):

            recovery_otp.attempts+=1

recovery_otp.save(
update_fields=["attempts"]
)

messages.error(
request,
"The SMS verification code is incorrect."
)

returnrender_stage(
"new_sms"
)





recovery_otp.is_verified=True

recovery_otp.save(
update_fields=["is_verified"]
)

request.session[
"recovery_sms_verified"
]=True





ifrequest.session.get(
"recovery_authenticator_verified"
):

            returncomplete_recovery_update()






two_factor=(
TwoFactorAuth.objects
.filter(
user=request.user,
is_enabled=True,
)
.first()
)

if(
two_factor
andtwo_factor.secret_key
):

            request.session[
"recovery_verification_stage"
]="authenticator"

request.session.modified=True

returnrender_stage(
"authenticator"
)





old_email=request.session.get(
"recovery_old_email"
)

old_phone=request.session.get(
"recovery_old_phone"
)

ifnotold_emailandnotold_phone:

            clear_recovery_session()

messages.error(
request,
"For security, you must enable authenticator two-factor authentication before establishing recovery information."
)

returnredirect(
"two_factor_setup"
)

returncomplete_recovery_update()





if(
request.method=="POST"
andrequest.POST.get("action")
=="verify_authenticator"
):

        ifnotrecovery_session_is_valid():

            returnsecurity_failure(
"Your recovery verification session has expired. Please start again."
)

code=request.POST.get(
"otp_code",
""
).strip()

ifnotcode.isdigit()orlen(code)!=6:

            messages.error(
request,
"Please enter the 6-digit authenticator code."
)

returnrender_stage(
"authenticator"
)

two_factor=(
TwoFactorAuth.objects
.filter(
user=request.user,
is_enabled=True,
)
.first()
)

if(
nottwo_factor
ornottwo_factor.secret_key
):

            returnsecurity_failure(
"Authenticator verification is unavailable. Please try again."
)





auth_rate_limit_key=(
f"recovery_auth_attempts:"
f"{request.user.id}:"
f"{request.META.get('REMOTE_ADDR','unknown')}"
)

attempts=cache.get(
auth_rate_limit_key,
0
)

ifattempts>=5:

            messages.error(
request,
"Too many incorrect authenticator attempts. Please try again later."
)

returnrender_stage(
"authenticator"
)





totp=pyotp.TOTP(
two_factor.secret_key
)

ifnottotp.verify(
code,
valid_window=1
):

            attempts+=1

cache.set(
auth_rate_limit_key,
attempts,
5*7*24*60*60
)

messages.error(
request,
"The authenticator code is incorrect."
)

returnrender_stage(
"authenticator"
)

cache.delete(
auth_rate_limit_key
)





request.session[
"recovery_authenticator_verified"
]=True





ifrequest.session.get(
"recovery_authenticator_first"
):

            request.session[
"recovery_authenticator_first"
]=False

new_email=request.session.get(
"pending_recovery_email"
)

ifnotnew_email:

                returnsecurity_failure(
"Recovery information is incomplete. Please start again."
)

ifnotcan_send_recovery_otp(
request,
"email",
"recovery_change",
):

                messages.error(
request,
"Please wait before requesting another email verification code."
)

returnrender_stage(
"authenticator"
)

_,email_otp=create_recovery_otp(
user=request.user,
channel="email",
purpose="recovery_change",
)

send_recovery_email_otp(
user=request.user,
email=new_email,
otp=email_otp,
)

request.session[
"recovery_verification_stage"
]="new_email"

request.session.modified=True

messages.success(
request,
"Authenticator verified. A verification code has been sent to your new recovery email."
)

returnrender_stage(
"new_email"
)






returncomplete_recovery_update()





if(
request.method=="POST"
andrequest.POST.get("action")
=="start_verification"
):

        current_password=request.POST.get(
"current_password",
""
)

email=request.POST.get(
"recovery_email",
""
).strip()

phone=request.POST.get(
"recovery_phone",
""
).strip()





ifnotrequest.user.check_password(
current_password
):

            messages.error(
request,
"Your current password is incorrect."
)

returnrender(
request,
"accounts/update_recovery.html"
)





ifemail:

            try:

                validate_email(email)

exceptValidationError:

                messages.error(
request,
"Please enter a valid recovery email address."
)

returnrender(
request,
"accounts/update_recovery.html"
)





ifphone:

            if(
len(phone)<7
orlen(phone)>20
):

                messages.error(
request,
"Please enter a valid recovery phone number."
)

returnrender(
request,
"accounts/update_recovery.html"
)





ifnotemailornotphone:

            messages.error(
request,
"Please provide both a recovery email and recovery phone number."
)

returnrender(
request,
"accounts/update_recovery.html"
)





two_factor=(
TwoFactorAuth.objects
.filter(
user=request.user,
is_enabled=True,
)
.first()
)

has_authenticator=bool(
two_factor
andtwo_factor.secret_key
)





old_email=(
profile.recovery_email
or""
).strip()

old_phone=(
profile.recovery_phone
or""
).strip()





if(
notold_email
andnotold_phone
andnothas_authenticator
):

            messages.error(
request,
"For security, please enable authenticator two-factor authentication before establishing recovery information."
)

returnredirect(
"two_factor_setup"
)





clear_recovery_session()





request.session.cycle_key()





request.session[
"pending_recovery_user_id"
]=request.user.id

request.session[
"pending_recovery_email"
]=email

request.session[
"pending_recovery_phone"
]=phone

request.session[
"recovery_old_email"
]=old_email

request.session[
"recovery_old_phone"
]=old_phone

request.session[
"recovery_started_at"
]=time.time()

request.session[
"recovery_old_email_verified"
]=False

request.session[
"recovery_old_sms_verified"
]=False

request.session[
"recovery_email_verified"
]=False

request.session[
"recovery_sms_verified"
]=False

request.session[
"recovery_authenticator_verified"
]=False

request.session[
"recovery_authenticator_first"
]=False





ifold_email:

            ifnotcan_send_recovery_otp(
request,
"email",
"recovery_authorization",
):

                clear_recovery_session()

messages.error(
request,
"Please wait before requesting another email verification code."
)

returnredirect(
"update_recovery"
)

_,email_otp=create_recovery_otp(
user=request.user,
channel="email",
purpose="recovery_authorization",
)

send_recovery_email_otp(
user=request.user,
email=old_email,
otp=email_otp,
)

request.session[
"recovery_verification_stage"
]="old_email"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your existing recovery email."
)

returnrender_stage(
"old_email"
)





ifold_phone:

            ifnotcan_send_recovery_otp(
request,
"sms",
"recovery_authorization",
):

                clear_recovery_session()

messages.error(
request,
"Please wait before requesting another SMS verification code."
)

returnredirect(
"update_recovery"
)

_,sms_otp=create_recovery_otp(
user=request.user,
channel="sms",
purpose="recovery_authorization",
)

send_recovery_sms_otp(
phone=old_phone,
otp=sms_otp,
)

request.session[
"recovery_verification_stage"
]="old_sms"

request.session.modified=True

messages.success(
request,
"A verification code has been sent to your existing recovery phone."
)

returnrender_stage(
"old_sms"
)



















ifhas_authenticator:

            request.session[
"recovery_authenticator_first"
]=True

request.session[
"recovery_verification_stage"
]="authenticator"

request.session.modified=True

messages.success(
request,
"Please verify your authenticator app to authorize the recovery setup."
)

returnrender_stage(
"authenticator"
)





clear_recovery_session()

messages.error(
request,
"Recovery verification could not be started. Please try again."
)

returnredirect(
"update_recovery"
)





returnrender(
request,
"accounts/update_recovery.html"
)

@login_required
defdownload_account_data(request):
    profile,_=(
UserProfile.objects.get_or_create(
user=request.user
)
)




wallets=(
Wallet.objects
.filter(user=request.user)
.order_by("currency")
)

wallet_balance=Decimal("0.00")

forwalletinwallets:
        available_asset=(
wallet.balance
-wallet.reserved_balance
)

ifavailable_asset<Decimal("0"):
            available_asset=Decimal("0")

asset_price=(
AssetPrice.objects
.filter(currency=wallet.currency)
.first()
)

ifnotasset_price:
            continue

exchange_rate=asset_price.usd_price

if(
exchange_rateisNone
ornotexchange_rate.is_finite()
orexchange_rate<=Decimal("0")
):
            continue

wallet_balance+=(
available_asset*exchange_rate
)

wallet_balance=wallet_balance.quantize(
Decimal("0.01")
)




investment_balance=(
Investment.objects
.filter(
user=request.user,
status="active",
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
)

investment_balance=investment_balance.quantize(
Decimal("0.01")
)




total_investment=(
Investment.objects
.filter(
user=request.user,
)
.aggregate(
total=Sum("amount_usd")
)["total"]
orDecimal("0.00")
)

total_investment=total_investment.quantize(
Decimal("0.01")
)




referral_earnings=(
Referral.objects
.filter(
user=request.user,
)
.aggregate(
total=Sum("commission_earned")
)["total"]
orDecimal("0.00")
)

referral_earnings=referral_earnings.quantize(
Decimal("0.01")
)




response=HttpResponse(
content_type="text/csv"
)

response["Content-Disposition"]=(
'attachment; filename="account_data.csv"'
)

writer=csv.writer(response)

writer.writerow(
[
"Field",
"Value",
]
)

writer.writerow(
[
"Username",
request.user.username,
]
)

writer.writerow(
[
"Name",
profile.nameor"",
]
)

writer.writerow(
[
"Email",
request.user.email,
]
)

writer.writerow(
[
"KYC Verified",
profile.kyc_verified,
]
)

writer.writerow(
[
"Total Balance",
wallet_balance,
]
)

writer.writerow(
[
"Investment Balance",
investment_balance,
]
)

writer.writerow(
[
"Referral Code",
profile.referral_codeor"",
]
)

writer.writerow(
[
"Referral Earnings",
referral_earnings,
]
)

writer.writerow(
[
"Total Investment",
total_investment,
]
)

returnresponse


defcalculate_gas_fee(plan_name,amount):

    ifplan_name=="Finbit Starter":
        return50

elifplan_name=="Infinity":
        return100

elifplan_name=="Finbit Titan":
        return300

elifplan_name=="Finbit Nova":
        return400

elifplan_name=="Elephant Wealth Plan":
        return900

elifplan_name=="Cobra Premium Plan":
        return4500

elifplan_name=="Lion Legacy Plan":
        return450

elifplan_name=="Tiger Legacy Plan":
        return450

return0


defexecute_trade(deposit):
    existing_trade=Trade.objects.filter(
deposit=deposit
).first()

ifexisting_trade:
        returnexisting_trade

result=(
"win"
ifrandom.randint(1,100)==1
else"lose"
)

gas_fee=None
profit_amount=None
payout_amount=None
gas_payment_status="not_required"

ifresult=="win":
        plan_name=deposit.plan.name
return_rate=str(
deposit.plan.return_rate
).strip()

amount=Decimal(
str(deposit.amount_usd)
)

normalized_rate=(
return_rate
.replace("Return","")
.replace("return","")
.strip()
)

ifnormalized_rate.endswith("%"):
            percentage=Decimal(
normalized_rate.rstrip("%").strip()
)

profit_amount=(
amount*percentage/Decimal("100")
)

elifnormalized_rate.upper().endswith("USD"):
            fixed_profit=(
normalized_rate[:-3].strip()
)

profit_amount=Decimal(
fixed_profit
)

else:
            profit_amount=Decimal("0")

payout_amount=(
amount+profit_amount
)

gas_fee=Decimal(
str(
calculate_gas_fee(
plan_name,
float(amount),
)
)
)

gas_payment_status="pending"

trade=Trade.objects.create(
deposit=deposit,
user=deposit.user,
plan=deposit.plan,
result=result,
gas_fee=gas_fee,
profit_amount=profit_amount,
payout_amount=payout_amount,
gas_payment_status=gas_payment_status,
)

returntrade

@login_required
deftrading_page(request):

    plans=InvestmentPlan.objects.all()

payment_methods=Deposit.PAYMENT_CHOICES

trades=(
Trade.objects
.filter(user=request.user)
.select_related(
"deposit",
"plan",
)
.order_by("-created_at")
)

latest_trade=trades.first()

withdrawals=(
Withdrawal.objects
.filter(
user=request.user,
source="live_trade",
)
.select_related(
"trade",
"wallet",
)
.order_by("-created_at")
)

latest_withdrawal=withdrawals.first()

ifrequest.method=="POST":

        plan_id=request.POST.get("plan_id")

payment_method=request.POST.get(
"payment_method"
)

amount=Decimal(
request.POST.get("amount","0")
)

plan=get_object_or_404(
InvestmentPlan,
id=plan_id,
)

ifamount<plan.minimum_investment:

            returnrender(
request,
"accounts/trading_page.html",
{
"plans":plans,
"payment_methods":payment_methods,
"trades":trades,
"latest_trade":latest_trade,
"withdrawals":withdrawals,
"latest_withdrawal":latest_withdrawal,
"error":(
"Amount is below the minimum investment."
),
},
)

if(
plan.maximum_investment
andamount>plan.maximum_investment
):

            returnrender(
request,
"accounts/trading_page.html",
{
"plans":plans,
"payment_methods":payment_methods,
"trades":trades,
"latest_trade":latest_trade,
"withdrawals":withdrawals,
"latest_withdrawal":latest_withdrawal,
"error":(
"Amount exceeds the maximum investment."
),
},
)

deposit=Deposit.objects.create(
user=request.user,
plan=plan,
payment_method=payment_method,
amount_usd=amount,
status="pending",
source="live_trade",
)

wallet=CompanyWallet.objects.filter(
currency=payment_method,
).first()

returnrender(
request,
"accounts/deposit_page.html",
{
"deposit":deposit,
"wallet":wallet,
},
)

returnrender(
request,
"accounts/trading_page.html",
{
"plans":plans,
"payment_methods":payment_methods,
"trades":trades,
"latest_trade":latest_trade,
"withdrawals":withdrawals,
"latest_withdrawal":latest_withdrawal,
},
)

@login_required
defconfirm_deposit(
request,
deposit_id,
):

    deposit=get_object_or_404(
Deposit,
id=deposit_id,
user=request.user,
)

ifrequest.method=="POST":

        deposit.proof=request.FILES.get(
"proof"
)

deposit.status="pending"

deposit.save()

returnrender(
request,
"accounts/waiting_for_admin.html",
{
"deposit":deposit,
},
)

returnredirect("trade")


@login_required
deftrade_result(request,trade_id):

    trade=get_object_or_404(
Trade.objects.select_related(
"deposit",
"plan",
),
id=trade_id,
user=request.user,
)

payment_methods=Deposit.PAYMENT_CHOICES

if(
request.method=="POST"
andtrade.result=="win"
andtrade.gas_payment_status=="pending"
andnothasattr(trade,"gas_payment")
):

        payment_method=request.POST.get(
"payment_method"
)

proof=request.FILES.get(
"proof"
)

ifpayment_methodnotindict(
Deposit.PAYMENT_CHOICES
):

            messages.error(
request,
"Select a valid payment method.",
)

returnredirect(
"trade_result",
trade_id=trade.id,
)

asset_price=(
AssetPrice.objects
.filter(
currency=payment_method,
)
.first()
)

if(
notasset_price
orasset_price.usd_price<=0
):

            messages.error(
request,
"Exchange rate is unavailable.",
)

returnredirect(
"trade_result",
trade_id=trade.id,
)

asset_amount=(
Decimal(str(trade.gas_fee))
/asset_price.usd_price
).quantize(
Decimal("0.000000000001")
)

TradeGasPayment.objects.create(
trade=trade,
user=request.user,
payment_method=payment_method,
amount_usd=trade.gas_fee,
asset_amount=asset_amount,
exchange_rate=asset_price.usd_price,
proof=proof,
)

messages.success(
request,
"Gas payment submitted successfully. It is awaiting admin approval.",
)

returnredirect(
"trade_result",
trade_id=trade.id,
)

returnrender(
request,
"accounts/trade_result.html",
{
"trade":trade,
"payment_methods":payment_methods,
},
)

@login_required
deftrade_history(request):

    trades=(
Trade.objects
.filter(user=request.user)
.order_by("-created_at")
)

returnrender(
request,
"accounts/trade_history.html",
{
"trades":trades,
},
)