fromdecimalimportDecimal
fromdjango.contrib.auth.formsimportUserCreationForm
fromdjangoimportforms
fromdjango.contrib.auth.modelsimportUser
fromdjango.contrib.authimportauthenticate
from.modelsimport(
KYCSubmission,
Wallet,
Deposit,
Withdrawal,
UserProfile,
)


classKYCForm(forms.ModelForm):

    classMeta:
        model=KYCSubmission
fields=["document"]

widgets={
"document":forms.ClearableFileInput(
attrs={
"accept":"image/*",
"capture":"environment",
}
)
}


classWalletForm(forms.ModelForm):

    classMeta:
        model=Wallet
fields=["currency","address"]

widgets={
"currency":forms.Select(
attrs={
"class":"form-control",
}
),
"address":forms.TextInput(
attrs={
"class":"form-control",
"placeholder":"Enter wallet address",
}
),
}


classDepositForm(forms.ModelForm):

    classMeta:
        model=Deposit

fields=[
"plan",
"amount_usd",
"proof",
"payment_method",
]

widgets={
"amount_usd":forms.NumberInput(
attrs={
"step":"0.01",
"min":"0.01",
"placeholder":"Enter amount in USD",
}
),
}

defclean(self):

        cleaned_data=super().clean()

plan=cleaned_data.get("plan")
amount_usd=cleaned_data.get("amount_usd")
payment_method=cleaned_data.get("payment_method")





ifnotpayment_method:
            self.add_error(
"payment_method",
"Please select a payment method.",
)





ifamount_usdisNone:
            self.add_error(
"amount_usd",
"Please enter a deposit amount.",
)

elifnotamount_usd.is_finite():
            self.add_error(
"amount_usd",
"Please enter a valid amount.",
)

elifamount_usd<=Decimal("0.00"):
            self.add_error(
"amount_usd",
"Amount must be greater than zero.",
)





if(
plan
andamount_usdisnotNone
andamount_usd.is_finite()
andamount_usd>Decimal("0.00")
):

            ifamount_usd<plan.minimum_investment:
                self.add_error(
"amount_usd",
(
f"Minimum deposit for {plan.name} "
f"is ${plan.minimum_investment}."
),
)

elif(
plan.maximum_investmentisnotNone
andamount_usd>plan.maximum_investment
):
                self.add_error(
"amount_usd",
(
f"Maximum deposit for {plan.name} "
f"is ${plan.maximum_investment}."
),
)

returncleaned_data



classDepositApprovalForm(forms.ModelForm):

    classMeta:
        model=Deposit
fields=["status"]

defclean_status(self):
        status=self.cleaned_data.get("status")

ifstatusnotin["approved","rejected"]:
            raiseforms.ValidationError(
"Please select a valid deposit status."
)

returnstatus




classWithdrawalForm(forms.ModelForm):

    WALLET_CHOICES=[
("BTC","Bitcoin (BTC)"),
("ETH","Ethereum (ETH)"),
("USDT_ERC20","Tether (USDT ERC20)"),
("USDT_TRC20","Tether (USDT TRC20)"),
]

wallet_currency=forms.ChoiceField(
choices=WALLET_CHOICES,
label="Withdraw From",
)

classMeta:
        model=Withdrawal

fields=[
"wallet_currency",
"amount_usd",
"destination_wallet",
]

widgets={
"amount_usd":forms.NumberInput(
attrs={
"step":"0.01",
"min":"6.00",
"placeholder":"Enter withdrawal amount in USD",
}
),
"destination_wallet":forms.TextInput(
attrs={
"placeholder":"Enter destination wallet address",
}
),
}

labels={
"amount_usd":"Withdrawal Amount (USD)",
"destination_wallet":"Destination Wallet",
}

defclean_amount_usd(self):

        amount_usd=self.cleaned_data.get(
"amount_usd"
)

ifamount_usdisNone:
            raiseforms.ValidationError(
"Please enter a withdrawal amount."
)

ifnotamount_usd.is_finite():
            raiseforms.ValidationError(
"Please enter a valid withdrawal amount."
)

ifamount_usd<=Decimal("0.00"):
            raiseforms.ValidationError(
"Withdrawal amount must be greater than zero."
)

ifamount_usd<Decimal("6.00"):
            raiseforms.ValidationError(
"Minimum withdrawal is $6."
)

returnamount_usd

defclean_wallet_currency(self):

        wallet_currency=self.cleaned_data.get(
"wallet_currency"
)

allowed_wallets={
"BTC",
"ETH",
"USDT_ERC20",
"USDT_TRC20",
}

ifwallet_currencynotinallowed_wallets:
            raiseforms.ValidationError(
"Please select a valid wallet."
)

returnwallet_currency


classProfilePictureForm(forms.ModelForm):

    classMeta:
        model=UserProfile
fields=["picture"]

widgets={
"picture":forms.FileInput(
attrs={
"class":"file-upload-input",
"accept":"image/*",
}
)
}


classSettingsForm(forms.Form):

    username=forms.CharField(
max_length=150,
label="Username",
)

email=forms.EmailField(
label="Email Address",
)

preferred_currency=forms.ChoiceField(
label="Preferred Investment Option",
choices=[
("BTC","Bitcoin (BTC)"),
("ETH","Ethereum (ETH)"),
("USDT_ERC20","Tether (USDT ERC20)"),
("USDT_TRC20","Tether (USDT TRC20)"),
],
)

risk_level=forms.ChoiceField(
label="Investment Risk Level",
choices=[
("low","Low"),
("medium","Medium"),
("high","High"),
],
)

notification_emails=forms.BooleanField(
label="Receive investment updates via email",
required=False,
)

two_factor_auth=forms.BooleanField(
label="Enable Two-Factor Authentication",
required=False,
)

def__init__(self,user,*args,**kwargs):

        super().__init__(*args,**kwargs)

self.user=user

self.fields["username"].initial=user.username

self.fields["email"].initial=user.email

self.fields["preferred_currency"].initial=getattr(
user,
"preferred_currency",
"BTC",
)

self.fields["risk_level"].initial=getattr(
user,
"risk_level",
"medium",
)

self.fields["notification_emails"].initial=getattr(
user,
"notification_emails",
True,
)

self.fields["two_factor_auth"].initial=getattr(
user,
"two_factor_auth",
False,
)

defclean_username(self):

        username=self.cleaned_data["username"]

existing_user=(
User.objects
.filter(username=username)
.exclude(pk=self.user.pk)
.first()
)

ifexisting_user:
            raiseforms.ValidationError(
"That username is already in use."
)

returnusername

defclean_email(self):

        email=self.cleaned_data["email"]

existing_user=(
User.objects
.filter(email=email)
.exclude(pk=self.user.pk)
.first()
)

ifexisting_user:
            raiseforms.ValidationError(
"That email address is already in use."
)

returnemail

defsave(self):

        self.user.username=self.cleaned_data["username"]

self.user.email=self.cleaned_data["email"]

ifhasattr(self.user,"preferred_currency"):
            self.user.preferred_currency=(
self.cleaned_data["preferred_currency"]
)

ifhasattr(self.user,"risk_level"):
            self.user.risk_level=(
self.cleaned_data["risk_level"]
)

ifhasattr(self.user,"notification_emails"):
            self.user.notification_emails=(
self.cleaned_data["notification_emails"]
)

ifhasattr(self.user,"two_factor_auth"):
            self.user.two_factor_auth=(
self.cleaned_data["two_factor_auth"]
)

self.user.save()

returnself.user


classSignupForm(UserCreationForm):
    email=forms.EmailField(
required=True,
widget=forms.EmailInput(
attrs={
"autocomplete":"email",
"placeholder":"Enter your email address",
}
),
)

classMeta:
        model=User
fields=(
"username",
"email",
"password1",
"password2",
)

classLoginForm(forms.Form):
    username=forms.CharField(
label="Username or Email",
widget=forms.TextInput(
attrs={
"placeholder":"Username or Email",
"autocomplete":"username",
}
),
)

password=forms.CharField(
label="Password",
widget=forms.PasswordInput(
attrs={
"placeholder":"Password",
"autocomplete":"current-password",
}
),
)

def__init__(self,request=None,*args,**kwargs):
        super().__init__(*args,**kwargs)

self.request=request
self.user_cache=None

defclean(self):
        cleaned_data=super().clean()

username_or_email=cleaned_data.get("username")
password=cleaned_data.get("password")

ifnotusername_or_emailornotpassword:
            returncleaned_data




user=authenticate(
self.request,
username=username_or_email,
password=password,
)




ifuserisNone:
            try:
                email_user=User.objects.get(
email__iexact=username_or_email
)
exceptUser.DoesNotExist:
                email_user=None
exceptUser.MultipleObjectsReturned:
                email_user=None

ifemail_user:
                user=authenticate(
self.request,
username=email_user.username,
password=password,
)




ifuserisNone:
            raiseforms.ValidationError(
"Invalid username/email or password."
)




ifnotuser.is_active:
            raiseforms.ValidationError(
"This account is inactive."
)

self.user_cache=user

returncleaned_data

defget_user(self):
        returnself.user_cache