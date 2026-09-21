from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from core.models import InvestmentPlan
from django.conf import settings
from decimal import Decimal


class SupportPage(models.Model):
    heading = models.CharField(max_length=200, default="Support Center")
    intro_text = models.TextField(blank=True, null=True)

    email_support = models.EmailField(default="support@example.com")
    phone_support = models.CharField(max_length=20, blank=True, null=True)
    live_chat_available = models.BooleanField(default=True)

    articles_text = models.TextField(
        default="We're currently preparing helpful guides and FAQs. Please check back soon."
    )
    account_help_text = models.TextField(
        default="Our support team is here to help you with deposits, withdrawals, wallet settings, investments, verification, and other account-related questions."
    )

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading


class DashboardMenu(models.Model):
    title = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    name = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)


    kyc_verified = models.BooleanField(default=False)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    investment_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referrer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referred_users"
    )
    referral_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


    total_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    recovery_email = models.EmailField(blank=True, null=True)
    recovery_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


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

    else:

        UserProfile.objects.get_or_create(
            user=instance
        )

        instance.userprofile.save()


class KYCSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to="kyc_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class QuickAction(models.Model):
    ACTION_CHOICES = [
        ("deposit", "Deposit"),
        ("investment", "Start Investment"),
        ("withdrawal", "Withdraw"),
    ]

    title = models.CharField(max_length=50)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    url_name = models.CharField(max_length=50, help_text="Django URL name for this action")
    icon = models.CharField(max_length=50, default="fa-solid fa-bolt")

    def __str__(self):
        return self.title


class Wallet(models.Model):
    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_TRC20", "USDT TRC20"),
        ("USDT_ERC20", "USDT ERC20"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wallets",
    )

    currency = models.CharField(
        max_length=20,
        choices=CURRENCY_CHOICES,
    )

    balance = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        default=0,
    )

    reserved_balance = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        default=0,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "currency"],
                name="unique_user_wallet_currency",
            )
        ]

    @property
    def available_balance(self):
        available = self.balance - self.reserved_balance

        return (
            available
            if available > 0
            else Decimal("0")
        )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.get_currency_display()}"
        )



class AssetPrice(models.Model):
    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_TRC20", "Tether TRC20"),
        ("USDT_ERC20", "Tether ERC20"),
    ]

    currency = models.CharField(
        max_length=20,
        choices=CURRENCY_CHOICES,
        unique=True,
    )

    usd_price = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        default=0,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.get_currency_display()} - ${self.usd_price}"


class CompanyWallet(models.Model):
    CURRENCY_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_TRC20", "USDT TRC20"),
        ("USDT_ERC20", "USDT ERC20"),
    ]
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    address = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to="company_wallets/", null=True, blank=True)

    def __str__(self):
        return f"{self.get_currency_display()} Wallet"



class Deposit(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    PAYMENT_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_TRC20", "Tether TRC20"),
        ("USDT_ERC20", "Tether ERC20"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deposits",
    )

    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.PROTECT,
        related_name="deposits",
        null=True,
        blank=True,
    )


    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )


    amount_usd = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )


    asset_amount = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )


    received_asset_amount = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
        help_text="Actual amount of cryptocurrency received and credited.",
    )


    exchange_rate = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )


    proof = models.ImageField(
        upload_to="deposits/proofs/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    source = models.CharField(
        max_length=30,
        default="deposit",
    )

    credited_to_wallet = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"${self.amount_usd} - "
            f"{self.get_payment_method_display()}"
        )


class Withdrawal(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdrawals",
    )

    wallet = models.ForeignKey(
    Wallet,
        on_delete=models.PROTECT,
        related_name="withdrawals",
        null=True,
        blank=True,
    )
    trade = models.OneToOneField(
        "Trade",
        on_delete=models.PROTECT,
        related_name="withdrawal",
        null=True,
        blank=True,
    )
    amount_usd = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    asset_amount = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    exchange_rate = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    destination_wallet = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    source = models.CharField(
        max_length=30,
        default="withdrawal",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        currency = self.wallet.currency if self.wallet else "â€”"

        return (
            f"{self.user.username} - "
            f"{currency} - "
            f"${self.amount_usd} - "
            f"{self.asset_amount or 'â€”'} "
            f"({self.status})"
        )


class Investment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="investments",
    )

    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.PROTECT,
        related_name="investments",
    )

    amount_usd = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="investments",
        null=True,
        blank=True,
    )

    asset_amount = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    exchange_rate = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)

            if (
                not self.end_date
                and self.plan
                and self.plan.duration
                and self.created_at
            ):
                duration = self.plan.duration.lower().strip()

                if "lifetime" not in duration:
                    parts = duration.split()
                    number = None

                    for part in parts:
                        try:
                            number = int(part)
                            break
                        except ValueError:
                            continue

                    if number:
                        if "week" in duration:
                            self.end_date = (
                                self.created_at
                                + timedelta(weeks=number)
                            )

                        elif "day" in duration:
                            self.end_date = (
                                self.created_at
                                + timedelta(days=number)
                            )

                        elif "hour" in duration:
                            self.end_date = (
                                self.created_at
                                + timedelta(hours=number)
                            )

                        elif "minute" in duration:
                            self.end_date = (
                                self.created_at
                                + timedelta(minutes=number)
                            )

                        type(self).objects.filter(
                            pk=self.pk
                        ).update(
                            end_date=self.end_date
                        )

            return

        if (
            not self.end_date
            and self.plan
            and self.plan.duration
            and self.created_at
        ):
            duration = self.plan.duration.lower().strip()

            if "lifetime" not in duration:
                parts = duration.split()
                number = None

                for part in parts:
                    try:
                        number = int(part)
                        break
                    except ValueError:
                        continue

                if number:
                    if "week" in duration:
                        self.end_date = (
                            self.created_at
                            + timedelta(weeks=number)
                        )

                    elif "day" in duration:
                        self.end_date = (
                            self.created_at
                            + timedelta(days=number)
                        )

                    elif "hour" in duration:
                        self.end_date = (
                            self.created_at
                            + timedelta(hours=number)
                        )

                    elif "minute" in duration:
                        self.end_date = (
                            self.created_at
                            + timedelta(minutes=number)
                        )

        super().save(*args, **kwargs)


    @property
    def currency(self):
        return self.wallet.currency if self.wallet else None

    @property
    def currency_display(self):
        return (
            self.wallet.get_currency_display()
            if self.wallet
            else "â€”"
        )

    def __str__(self):
        currency = (
            self.wallet.currency
            if self.wallet
            else "â€”"
        )

        return (
            f"{self.user.username} - "
            f"{self.plan.name} - "
            f"${self.amount_usd} "
            f"({currency})"
        )


class Profit(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profits",
    )

    investment = models.ForeignKey(
        "Investment",
        on_delete=models.CASCADE,
        related_name="profits",
        null=True,
        blank=True,
    )

    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.CASCADE,
        related_name="profits",
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    payout_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="approved",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["investment", "payout_at"],
                name="unique_investment_payout",
            ),
        ]
        ordering = ["-payout_at"]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.plan.name} - "
            f"${self.amount} "
            f"({self.status})"
        )
    
class Bonus(models.Model):
    BONUS_TYPE_CHOICES = [
        ("welcome", "Welcome Bonus"),
        ("investment", "Investment Bonus"),
        ("promotion", "Promotional Bonus"),
        ("manual", "Manual Bonus"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bonuses"
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2
    )
    bonus_type = models.CharField(
        max_length=20,
        choices=BONUS_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.get_bonus_type_display()}"

class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referred_by")
    created_at = models.DateTimeField(auto_now_add=True)
    commission_earned = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} referred {self.referred_user.username}"



class ProfilePage(models.Model):
    heading = models.CharField(max_length=200, default="My Profile")
    subheading = models.CharField(max_length=300, default="Manage your account, investments, security and wallets")

    personal_info_heading = models.CharField(max_length=200, default="Personal Information")
    investment_summary_heading = models.CharField(max_length=200, default="Investment Summary")
    recent_investments_heading = models.CharField(max_length=200, default="Recent Investments")
    quick_actions_heading = models.CharField(max_length=200, default="Quick Actions")
    referral_heading = models.CharField(max_length=200, default="Referral Program")
    account_settings_heading = models.CharField(max_length=200, default="Account Settings")

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading





class InvestmentPageContent(models.Model):

    hero_title = models.CharField(
        max_length=200,
        default="Start Your Investment Journey"
    )

    hero_subtitle = models.TextField(
        default="Choose an investment plan that matches your goals and invest from your approved balance."
    )

    balance_label = models.CharField(
        max_length=100,
        default="Available Balance"
    )

    how_title = models.CharField(
        max_length=200,
        default="How Your Investment Works"
    )

    how_subtitle = models.TextField(
        default="A simple, transparent process designed to make investing straightforward."
    )

    calculator_title = models.CharField(
        max_length=200,
        default="Investment Calculator"
    )

    calculator_subtitle = models.TextField(
        default="Estimate your potential return before you invest."
    )

    security_title = models.CharField(
        max_length=200,
        default="Built Around Security & Transparency"
    )

    security_text = models.TextField(
        default="Your account information and investment activity are handled through our secure platform."
    )

    terms_title = models.CharField(
        max_length=200,
        default="Important Investment Information"
    )

    terms_text = models.TextField(
        default="Investment returns, durations and conditions vary by plan. Please review the details of each plan carefully before investing."
    )

    faq_title = models.CharField(
        max_length=200,
        default="Frequently Asked Questions"
    )

    support_title = models.CharField(
        max_length=200,
        default="Need Help Before You Invest?"
    )

    support_text = models.TextField(
        default="Our support team is available to help you understand the investment process."
    )

    support_button_text = models.CharField(
        max_length=100,
        default="Contact Support"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Investment Page Content"


class InvestmentHowItWorks(models.Model):

    title = models.CharField(max_length=150)

    description = models.TextField()

    icon = models.CharField(
        max_length=50,
        default="1"
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class InvestmentFeature(models.Model):

    title = models.CharField(max_length=150)

    description = models.TextField()

    icon = models.CharField(
        max_length=50,
        default="âœ“"
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class InvestmentFAQ(models.Model):

    question = models.CharField(max_length=300)

    answer = models.TextField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question

class SecurityCenterContent(models.Model):
    hero_title = models.CharField(
        max_length=200,
        default="Security Center"
    )
    hero_subtitle = models.TextField(
        default="Protect your account with advanced security, verification, and activity controls."
    )

    twofa_title = models.CharField(
        max_length=200,
        default="Two-Factor Authentication"
    )
    twofa_text = models.TextField(
        default="Add an extra layer of protection to your account using two-factor authentication."
    )

    compliance_title = models.CharField(
        max_length=200,
        default="Compliance & Verification"
    )
    compliance_text = models.TextField(
        default="Complete identity verification to help keep your account secure and compliant."
    )

    activity_title = models.CharField(
        max_length=200,
        default="Device & Activity"
    )
    activity_text = models.TextField(
        default="Review recent login activity and manage active sessions connected to your account."
    )

    controls_title = models.CharField(
        max_length=200,
        default="User Controls"
    )
    controls_text = models.TextField(
        default="Manage your password, recovery options, and API access from one secure location."
    )

    alerts_title = models.CharField(
        max_length=200,
        default="Security Alerts"
    )
    alerts_text = models.TextField(
        default="Monitor suspicious login attempts, unusual activity, and withdrawal security alerts."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Security Center Content"

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="two_factor"
    )

    is_enabled = models.BooleanField(default=False)

    secret_key = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def get_secret(self):
        """
        Return the user's TOTP secret.
        Generate one if it does not exist yet.
        """
        if not self.secret_key:
            self.secret_key = pyotp.random_base32()
            self.save(update_fields=["secret_key"])

        return self.secret_key

    def get_totp(self):
        """
        Return the TOTP generator for this account.
        """
        return pyotp.TOTP(self.get_secret())

    def provisioning_uri(self):
        """
        Generate the URI used to configure an authenticator app.
        """
        return self.get_totp().provisioning_uri(
            name=self.user.email or self.user.username,
            issuer_name="Finbit",
        )

    def verify_token(self, token):
        """
        Verify a TOTP token.

        valid_window=1 allows the immediately previous or next
        30-second time window to account for small clock differences.
        """
        if not token:
            return False

        return self.get_totp().verify(
            token,
            valid_window=1,
        )

    def __str__(self):
        return f"2FA - {self.user.username}"


class RecoveryOTP(models.Model):
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
    ]

    PURPOSE_CHOICES = [
        (
            "recovery_authorization",
            "Recovery Change Authorization",
        ),
        (
            "recovery_change",
            "Recovery Information Change",
        ),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recovery_otps",
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
    )

    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES,
    )

    code_hash = models.CharField(
        max_length=128,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveIntegerField(
        default=0,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.channel.upper()} OTP - "
            f"{self.user.username}"
        )


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey("Announcement", on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

class AnnouncementReply(models.Model):
    announcement = models.ForeignKey("Announcement", on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read_by_admin = models.BooleanField(default=False)
    is_read_by_user = models.BooleanField(default=False)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.announcement.title}"




class Notification(models.Model):

    TYPE_CHOICES = [
        ("general", "General"),
        ("signup", "Signup"),
        ("verification", "Verification"),
        ("deposit", "Deposit"),
        ("investment", "Investment"),
        ("withdrawal", "Withdrawal"),
        ("referral", "Referral"),
        ("bonus", "Bonus"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default="general",
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Trade(models.Model):

    RESULT_CHOICES = [
        ("win", "Win"),
        ("lose", "Lose"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    plan = models.ForeignKey(
        "core.InvestmentPlan",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    historical_plan_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    deposit = models.OneToOneField(
        "Deposit",
        on_delete=models.CASCADE,
        related_name="trade",
        null=True,
        blank=True,
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
    )

    gas_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    profit_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    payout_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    gas_payment_status = models.CharField(
        max_length=20,
        default="not_required",
    )

    payout_released = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):

        if (
            self.plan
            and not self.historical_plan_name
        ):
            self.historical_plan_name = self.plan.name

        super().save(*args, **kwargs)

    @property
    def plan_display_name(self):

        if self.plan:
            return self.plan.name

        return self.historical_plan_name or "Unknown Plan"

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.plan_display_name} - "
            f"{self.result}"
        )


class TradeGasPayment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    PAYMENT_CHOICES = [
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT_TRC20", "USDT TRC20"),
        ("USDT_ERC20", "USDT ERC20"),
    ]

    trade = models.OneToOneField(
        "Trade",
        on_delete=models.CASCADE,
        related_name="gas_payment",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trade_gas_payments",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )

    amount_usd = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    asset_amount = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    exchange_rate = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        null=True,
        blank=True,
    )

    proof = models.ImageField(
        upload_to="trade_gas/proofs/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"Trade #{self.trade.id} - "
            f"${self.amount_usd}"
        )


