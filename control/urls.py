from django.urls import path
from . import views
from control.views import (
investment_plans_view,
update_plan_view,
)

urlpatterns = [

    path(
        "dashboard/",
        views.dashboard_view,
        name="admin_dashboard",
    ),

    path(
        "investment-plans/",
        investment_plans_view,
        name="investment_plans",
    ),

    path(
        "investment-plans/<int:plan_id>/update/",
        update_plan_view,
        name="update_plan",
    ),

    path(
        "records/",
        views.records_view,
        name="records",
    ),

    path(
        "payment-methods/",
        views.payment_methods_view,
        name="payment_methods",
    ),

    path(
        "payment-methods/<int:wallet_id>/update/",
        views.update_wallet_view,
        name="update_wallet",
    ),

    path(
        "finance/deposits/",
        views.deposits_view,
        name="deposits",
    ),

    path(
        "finance/deposits/<int:deposit_id>/",
        views.deposit_detail_view,
        name="deposit_detail",
    ),

    path(
        "finance/investments/",
        views.investments_view,
        name="investments",
    ),

    path(
        "admin/transactions/",
        views.all_transactions_view,
        name="all_transactions",
    ),

    path(
        "finance/withdrawals/",
        views.withdrawals_view,
        name="withdrawals",
    ),

    path(
        "finance/withdrawals/<int:withdrawal_id>/approve/",
        views.approve_withdrawal,
        name="approve_withdrawal",
    ),

    path(
        "finance/withdrawals/<int:withdrawal_id>/reject/",
        views.reject_withdrawal,
        name="reject_withdrawal",
    ),

    path(
        "admin/verifications/",
        views.user_verifications_view,
        name="user_verifications",
    ),

    path(
        "admin/verifications/<int:submission_id>/",
        views.kyc_detail_view,
        name="kyc_detail",
    ),

    path(
        "admin/verifications/<int:submission_id>/approve/",
        views.approve_kyc,
        name="approve_kyc",
    ),

    path(
        "admin/verifications/<int:submission_id>/reject/",
        views.reject_kyc,
        name="reject_kyc",
    ),

    path(
        "user-wallets/",
        views.user_wallets_view,
        name="user_wallets",
    ),

    path(
        "announcements/",
        views.admin_announcements_view,
        name="admin_announcements",
    ),

    path(
        "announcements/<int:announcement_id>/",
        views.admin_announcement_detail_view,
        name="admin_announcement_detail",
    ),

    path(
        "settings/",
        views.settings_view,
        name="admin_settings",
    ),

    path(
        "user/<int:user_id>/detail/",
        views.admin_user_detail_view,
        name="admin_user_detail",
    ),

    path(
        "user/<int:user_id>/adjust-wallet/",
        views.admin_adjust_wallet_view,
        name="admin_adjust_wallet",
    ),

    path(
        "admin/login/",
        views.admin_login_view,
        name="admin_login",
    ),

    path(
        "admin/logout/",
        views.admin_logout_view,
        name="admin_logout",
    ),

    path(
        "finance/live-trading/",
        views.approve_deposits,
        name="approve_deposits",
    ),

    path(
        "finance/live-trading/<int:deposit_id>/approve/",
        views.approve_deposit,
        name="approve_deposit",
    ),

    path(
        "finance/live-trading/trade/<int:trade_id>/",
        views.trade_detail,
        name="trade_detail",
    ),

    path(
        "finance/live-trading/gas-payments/",
        views.trade_gas_payments,
        name="trade_gas_payments",
    ),

    path(
        "finance/live-trading/gas-payments/<int:payment_id>/approve/",
        views.approve_trade_gas_payment,
        name="approve_trade_gas_payment",
    ),

    path(
        "finance/live-trading/withdrawals/",
        views.live_trade_withdrawals_view,
        name="live_trade_withdrawals",
    ),

    path(
        "finance/live-trading/withdrawals/<int:withdrawal_id>/approve/",
        views.approve_live_trade_withdrawal,
        name="approve_live_trade_withdrawal",
    ),

    path(
        "finance/live-trading/withdrawals/<int:withdrawal_id>/reject/",
        views.reject_live_trade_withdrawal,
        name="reject_live_trade_withdrawal",
    ),

    path(
        "security-settings/",
        views.security_settings_view,
        name="security_settings",
    ),

    path(
        "security-settings/qr-code/",
        views.security_qr_code_view,
        name="security_qr_code",
    ),

    path(
        "security-settings/enable-2fa/",
        views.enable_two_factor_view,
        name="enable_two_factor",
    ),

    path(
        "security-settings/recovery-codes/",
        views.generate_recovery_codes_view,
        name="generate_recovery_codes",
    ),

    path(
        "security-settings/enable-2fa/",
        views.enable_two_factor_view,
        name="enable_two_factor",
    ),

    path(
        "security-settings/disable-2fa/",
        views.disable_two_factor_view,
        name="disable_two_factor",
    ),

]
