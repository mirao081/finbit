from django.contrib import admin

from .models import (
    DashboardMenu,
    UserProfile,
    QuickAction,
    Wallet,
    CompanyWallet,
    Deposit,
    Profit,
    Referral,
    SupportPage,
    ProfilePage,
    InvestmentPageContent,
    InvestmentHowItWorks,
    InvestmentFeature,
    InvestmentFAQ,
    SecurityCenterContent,
    Announcement,
    Withdrawal,
)


@admin.register(DashboardMenu)
class DashboardMenuAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "url_name",
        "order",
    )

    ordering = (
        "order",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "kyc_verified",
        "total_balance",
        "investment_balance",
    )


@admin.register(QuickAction)
class QuickActionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "action_type",
        "url_name",
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "currency",
        "balance",
        "reserved_balance",
        "address",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "currency",
        "address",
    )

    list_filter = (
        "currency",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(CompanyWallet)
class CompanyWalletAdmin(admin.ModelAdmin):

    list_display = (
        "currency",
        "address",
    )

    search_fields = (
        "currency",
        "address",
    )


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "plan",
        "payment_method",
        "amount_usd",
        "asset_amount",
        "received_asset_amount",
        "status",
        "credited_to_wallet",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "credited_to_wallet",
        "plan",
    )

    search_fields = (
        "user__username",
        "plan__name",
    )

    readonly_fields = (
        "created_at",
        "approved_at",
        "asset_amount",
        "exchange_rate",
        "received_asset_amount",
    )

    list_editable = (
        "status",
    )


@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "plan",
        "amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "plan",
    )

    search_fields = (
        "user__username",
        "plan__name",
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "referred_user",
        "commission_earned",
        "created_at",
    )

    search_fields = (
        "user__username",
        "referred_user__username",
    )

    list_filter = (
        "created_at",
    )


@admin.register(SupportPage)
class SupportPageAdmin(admin.ModelAdmin):

    list_display = (
        "heading",
        "email_support",
        "phone_support",
        "last_updated",
    )

    search_fields = (
        "heading",
        "intro_text",
        "articles_text",
        "account_help_text",
    )


@admin.register(ProfilePage)
class ProfilePageAdmin(admin.ModelAdmin):

    list_display = (
        "heading",
        "subheading",
        "last_updated",
    )


@admin.register(InvestmentPageContent)
class InvestmentPageContentAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Hero Section",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "balance_label",
                )
            },
        ),
        (
            "How It Works",
            {
                "fields": (
                    "how_title",
                    "how_subtitle",
                )
            },
        ),
        (
            "Investment Calculator",
            {
                "fields": (
                    "calculator_title",
                    "calculator_subtitle",
                )
            },
        ),
        (
            "Security Section",
            {
                "fields": (
                    "security_title",
                    "security_text",
                )
            },
        ),
        (
            "Important Information",
            {
                "fields": (
                    "terms_title",
                    "terms_text",
                )
            },
        ),
        (
            "FAQ",
            {
                "fields": (
                    "faq_title",
                )
            },
        ),
        (
            "Support",
            {
                "fields": (
                    "support_title",
                    "support_text",
                    "support_button_text",
                )
            },
        ),
    )

    readonly_fields = (
        "updated_at",
    )


@admin.register(InvestmentHowItWorks)
class InvestmentHowItWorksAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "order",
    )


@admin.register(InvestmentFeature)
class InvestmentFeatureAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "order",
    )


@admin.register(InvestmentFAQ)
class InvestmentFAQAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "order",
    )


@admin.register(SecurityCenterContent)
class SecurityCenterContentAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Hero Section",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                )
            },
        ),
        (
            "Two-Factor Authentication",
            {
                "fields": (
                    "twofa_title",
                    "twofa_text",
                )
            },
        ),
        (
            "Compliance & Verification",
            {
                "fields": (
                    "compliance_title",
                    "compliance_text",
                )
            },
        ),
        (
            "Device & Activity",
            {
                "fields": (
                    "activity_title",
                    "activity_text",
                )
            },
        ),
        (
            "User Controls",
            {
                "fields": (
                    "controls_title",
                    "controls_text",
                )
            },
        ),
        (
            "Security Alerts",
            {
                "fields": (
                    "alerts_title",
                    "alerts_text",
                )
            },
        ),
    )

    readonly_fields = (
        "updated_at",
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "created_at",
        "is_active",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
    )


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "wallet",
        "amount_usd",
        "asset_amount",
        "exchange_rate",
        "destination_wallet",
        "status",
        "created_at",
        "approved_at",
    )

    list_filter = (
        "status",
        "wallet__currency",
        "created_at",
    )

    search_fields = (
        "user__username",
        "destination_wallet",
        "wallet__address",
    )

    readonly_fields = (
        "created_at",
        "approved_at",
        "asset_amount",
        "exchange_rate",
    )