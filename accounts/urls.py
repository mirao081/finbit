fromdjango.urlsimportpath
fromdjango.contrib.authimportviewsasauth_views
from.importviews

urlpatterns=[

path(
"login/",
views.UserLoginView.as_view(),
name="login",
),

path(
"logout/",
views.user_logout,
name="logout",
),

path(
"dashboard/",
views.dashboard,
name="dashboard",
),

path(
"wallets/",
views.wallets,
name="wallets",
),

path(
"wallets/edit/<int:wallet_id>/",
views.edit_wallet,
name="edit_wallet",
),

path(
"wallets/delete/<int:wallet_id>/",
views.delete_wallet,
name="delete_wallet",
),

path(
"wallets/confirm-delete/<int:wallet_id>/",
views.confirm_delete_wallet,
name="confirm_delete_wallet",
),

path(
"deposit/",
views.deposit,
name="deposit",
),

path(
"deposit/invoice/<int:deposit_id>/",
views.deposit_invoice,
name="deposit_invoice",
),

path(
"start-investment/",
views.start_investment,
name="start_investment",
),

path(
"withdraw/",
views.withdraw,
name="withdraw",
),

path(
"withdraw/confirm/",
views.withdraw_invoice,
name="withdraw_invoice",
),

path(
"withdraw/confirm/submit/",
views.confirm_withdrawal,
name="confirm_withdrawal",
),

path(
"withdraw/success/<int:withdrawal_id>/",
views.withdrawal_confirmation_success,
name="withdrawal_confirmation_success",
),

path(
"transactions/",
views.transactions,
name="transactions",
),

path(
"transactions/",
views.transactions,
name="user_transactions",
),

path(
"profit-history/",
views.profit_history,
name="profit_history",
),

path(
"referrals/",
views.referrals,
name="referrals",
),

path(
"markets/",
views.markets,
name="markets",
),

path(
"support/",
views.support,
name="support",
),

path(
"profile/",
views.profile,
name="profile",
),

path(
"security-center/",
views.security_center,
name="security_center",
),

path(
"update-recovery/",
views.update_recovery,
name="update_recovery",
),

path(
"download-account-data/",
views.download_account_data,
name="download_account_data",
),

path(
"login-activity/",
views.login_activity,
name="login_activity",
),

path(
"revoke-sessions/",
views.revoke_sessions,
name="revoke_sessions",
),

path(
"password-change/",
auth_views.PasswordChangeView.as_view(
template_name="accounts/password_change.html"
),
name="password_change",
),

path(
"password-change/done/",
auth_views.PasswordChangeDoneView.as_view(
template_name="accounts/password_change_done.html"
),
name="password_change_done",
),

path(
"password-reset/",
auth_views.PasswordResetView.as_view(
template_name="accounts/password_reset.html"
),
name="password_reset",
),

path(
"password-reset/done/",
auth_views.PasswordResetDoneView.as_view(
template_name="accounts/password_reset_done.html"
),
name="password_reset_done",
),

path(
"reset/<uidb64>/<token>/",
auth_views.PasswordResetConfirmView.as_view(
template_name="accounts/password_reset_confirm.html"
),
name="password_reset_confirm",
),

path(
"reset/done/",
auth_views.PasswordResetCompleteView.as_view(
template_name="accounts/password_reset_complete.html"
),
name="password_reset_complete",
),

path(
"settings/delete/",
views.delete_account,
name="delete_account",
),

path(
"account-deleted/",
views.account_deleted,
name="account_deleted",
),

path(
"settings/",
views.account_settings,
name="settings",
),

path(
"announcements/",
views.announcements,
name="announcements",
),

path(
"kyc-verification/",
views.kyc_verification,
name="kyc_verification",
),

path(
"performance-data/",
views.performance_data,
name="performance_data",
),

path(
"two-factor/setup/",
views.two_factor_setup,
name="two_factor_setup",
),

path(
"two-factor/login/",
views.two_factor_login,
name="two_factor_login",
),

path(
"notifications/",
views.notifications,
name="notifications",
),

path(
"notifications/<int:notification_id>/read/",
views.mark_notification_read,
name="mark_notification_read",
),

path(
"notifications/read-all/",
views.mark_all_notifications_read,
name="mark_all_notifications_read",
),
path(
"trade/",
views.trading_page,
name="trade",
),

path(
"deposit/<int:deposit_id>/confirm/",
views.confirm_deposit,
name="confirm_deposit",
),

path(
"trade/result/<int:trade_id>/",
views.trade_result,
name="trade_result",
),

path(
"trade/history/",
views.trade_history,
name="trade_history",
),
path(
"live-trade/withdraw/<int:trade_id>/",
views.live_trade_withdrawal,
name="live_trade_withdrawal",
),
]