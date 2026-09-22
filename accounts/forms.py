from decimal import Decimal

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import (
    KYCSubmission,
    Wallet,
    Deposit,
    Withdrawal,
    UserProfile,
)


class KYCForm(forms.ModelForm):

    class Meta:
        model = KYCSubmission
        fields = ["document"]

        widgets = {
            "document": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                    "capture": "environment",
                }
            )
        }


class WalletForm(forms.ModelForm):

    class Meta:
        model = Wallet
        fields = ["currency", "address"]

        widgets = {
            "currency": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter wallet address",
                }
            ),
        }


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit

        fields = [
            "plan",
            "amount_usd",
            "proof",
            "payment_method",
        ]

        widgets = {
            "amount_usd": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter amount in USD",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        plan = cleaned_data.get("plan")
        amount_usd = cleaned_data.get("amount_usd")
        payment_method = cleaned_data.get("payment_method")

        if not payment_method:
            self.add_error(
                "payment_method",
                "Please select a payment method.",
            )

        if amount_usd is None:
            self.add_error(
                "amount_usd",
                "Please enter a deposit amount.",
            )

        elif not amount_usd.is_finite():
            self.add_error(
                "amount_usd",
                "Please enter a valid amount.",
            )

        elif amount_usd <= Decimal("0.00"):
            self.add_error(
                "amount_usd",
                "Amount must be greater than zero.",
            )

        if (
            plan
            and amount_usd is not None
            and amount_usd.is_finite()
            and amount_usd > Decimal("0.00")
        ):

            if amount_usd < plan.minimum_investment:
                self.add_error(
                    "amount_usd",
                    (
                        f"Minimum deposit for {plan.name} "
                        f"is ${plan.minimum_investment}."
                    ),
                )

            elif (
                plan.maximum_investment is not None
                and amount_usd > plan.maximum_investment
            ):
                self.add_error(
                    "amount_usd",
                    (
                        f"Maximum deposit for {plan.name} "
                        f"is ${plan.maximum_investment}."
                    ),
                )

        return cleaned_data


class DepositApprovalForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = ["status"]

    def clean_status(self):

        status = self.cleaned_data.get("status")

        if status not in ["approved", "rejected"]:
            raise forms.ValidationError(
                "Please select a valid deposit status."
            )

        return status


class WithdrawalForm(forms.ModelForm):

    WALLET_CHOICES = [
        ("BTC", "Bitcoin (BTC)"),
        ("ETH", "Ethereum (ETH)"),
        ("USDT_ERC20", "Tether (USDT ERC20)"),
        ("USDT_TRC20", "Tether (USDT TRC20)"),
    ]

    wallet_currency = forms.ChoiceField(
        choices=WALLET_CHOICES,
        label="Withdraw From",
    )

    class Meta:
        model = Withdrawal

        fields = [
            "wallet_currency",
            "amount_usd",
            "destination_wallet",
        ]

        widgets = {
            "amount_usd": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "6.00",
                    "placeholder": "Enter withdrawal amount in USD",
                }
            ),
            "destination_wallet": forms.TextInput(
                attrs={
                    "placeholder": "Enter destination wallet address",
                }
            ),
        }

        labels = {
            "amount_usd": "Withdrawal Amount (USD)",
            "destination_wallet": "Destination Wallet",
        }

    def clean_amount_usd(self):

        amount_usd = self.cleaned_data.get(
            "amount_usd"
        )

        if amount_usd is None:
            raise forms.ValidationError(
                "Please enter a withdrawal amount."
            )

        if not amount_usd.is_finite():
            raise forms.ValidationError(
                "Please enter a valid withdrawal amount."
            )

        if amount_usd <= Decimal("0.00"):
            raise forms.ValidationError(
                "Withdrawal amount must be greater than zero."
            )

        if amount_usd < Decimal("6.00"):
            raise forms.ValidationError(
                "Minimum withdrawal is $6."
            )

        return amount_usd

    def clean_wallet_currency(self):

        wallet_currency = self.cleaned_data.get(
            "wallet_currency"
        )

        allowed_wallets = {
            "BTC",
            "ETH",
            "USDT_ERC20",
            "USDT_TRC20",
        }

        if wallet_currency not in allowed_wallets:
            raise forms.ValidationError(
                "Please select a valid wallet."
            )

        return wallet_currency


class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["picture"]

        widgets = {
            "picture": forms.FileInput(
                attrs={
                    "class": "file-upload-input",
                    "accept": "image/*",
                }
            )
        }


class SettingsForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="Username",
    )

    email = forms.EmailField(
        label="Email Address",
    )

    preferred_currency = forms.ChoiceField(
        label="Preferred Investment Option",
        choices=[
            ("BTC", "Bitcoin (BTC)"),
            ("ETH", "Ethereum (ETH)"),
            ("USDT_ERC20", "Tether (USDT ERC20)"),
            ("USDT_TRC20", "Tether (USDT TRC20)"),
        ],
    )

    risk_level = forms.ChoiceField(
        label="Investment Risk Level",
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )

    notification_emails = forms.BooleanField(
        label="Receive investment updates via email",
        required=False,
    )

    two_factor_auth = forms.BooleanField(
        label="Enable Two-Factor Authentication",
        required=False,
    )

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["username"].initial = user.username

        self.fields["email"].initial = user.email

        self.fields["preferred_currency"].initial = getattr(
            user,
            "preferred_currency",
            "BTC",
        )

        self.fields["risk_level"].initial = getattr(
            user,
            "risk_level",
            "medium",
        )

        self.fields["notification_emails"].initial = getattr(
            user,
            "notification_emails",
            True,
        )

        self.fields["two_factor_auth"].initial = getattr(
            user,
            "two_factor_auth",
            False,
        )

    def clean_username(self):

        username = self.cleaned_data["username"]

        existing_user = (
            User.objects
            .filter(username=username)
            .exclude(pk=self.user.pk)
            .first()
        )

        if existing_user:
            raise forms.ValidationError(
                "That username is already in use."
            )

        return username

    def clean_email(self):

        email = self.cleaned_data["email"]

        existing_user = (
            User.objects
            .filter(email=email)
            .exclude(pk=self.user.pk)
            .first()
        )

        if existing_user:
            raise forms.ValidationError(
                "That email address is already in use."
            )

        return email

    def save(self):

        self.user.username = self.cleaned_data["username"]

        self.user.email = self.cleaned_data["email"]

        if hasattr(self.user, "preferred_currency"):
            self.user.preferred_currency = (
                self.cleaned_data["preferred_currency"]
            )

        if hasattr(self.user, "risk_level"):
            self.user.risk_level = (
                self.cleaned_data["risk_level"]
            )

        if hasattr(self.user, "notification_emails"):
            self.user.notification_emails = (
                self.cleaned_data["notification_emails"]
            )

        if hasattr(self.user, "two_factor_auth"):
            self.user.two_factor_auth = (
                self.cleaned_data["two_factor_auth"]
            )

        self.user.save()

        return self.user


class SignupForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Enter your email address",
            }
        ),
    )

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username or Email",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.request = request
        self.user_cache = None

    def clean(self):

        cleaned_data = super().clean()

        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username_or_email or not password:
            return cleaned_data

        user = authenticate(
            self.request,
            username=username_or_email,
            password=password,
        )

        if user is None:

            try:
                email_user = User.objects.get(
                    email__iexact=username_or_email
                )

            except User.DoesNotExist:
                email_user = None

            except User.MultipleObjectsReturned:
                email_user = None

            if email_user:
                user = authenticate(
                    self.request,
                    username=email_user.username,
                    password=password,
                )

        if user is None:
            raise forms.ValidationError(
                "Invalid username/email or password."
            )

        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive."
            )

        self.user_cache = user

        return cleaned_data

    def get_user(self):
        return self.user_cache