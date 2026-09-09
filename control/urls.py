from django.urls import path
from . import views
from control.views import investment_plans_view, update_plan_view

urlpatterns = [
               
    path("dashboard/", views.dashboard_view, name="admin_dashboard"),

                      
    path("investment-plans/", investment_plans_view, name="investment_plans"),
    path("investment-plans/<int:plan_id>/update/", update_plan_view, name="update_plan"),

             
    path("records/", views.records_view, name="records"),

                     
    path("payment-methods/", views.payment_methods_view, name="payment_methods"),
    path("payment-methods/<int:wallet_id>/update/", views.update_wallet_view, name="update_wallet"),

             
    path("finance/deposits/", views.deposits_view, name="deposits"),
    path("finance/deposits/<int:deposit_id>/", views.deposit_detail_view, name="deposit_detail"),                 
    path("finance/investments/", views.investments_view, name="investments"),
    path("admin/transactions/", views.all_transactions_view, name="all_transactions"),
    path("finance/withdrawals/", views.withdrawals_view, name="withdrawals"), 
    path("finance/withdrawals/<int:withdrawal_id>/approve/", views.approve_withdrawal, name="approve_withdrawal"),
    path("finance/withdrawals/<int:withdrawal_id>/reject/", views.reject_withdrawal, name="reject_withdrawal"),

                             
    path("admin/verifications/", views.user_verifications_view, name="user_verifications"),
    path("admin/verifications/<int:submission_id>/", views.kyc_detail_view, name="kyc_detail"),
    path("admin/verifications/<int:submission_id>/approve/", views.approve_kyc, name="approve_kyc"),
    path("admin/verifications/<int:submission_id>/reject/", views.reject_kyc, name="reject_kyc"),


                  
    path("user-wallets/", views.user_wallets_view, name="user_wallets"),

                    
                     
    path("announcements/", views.admin_announcements_view, name="admin_announcements"),
                     
    path("announcements/<int:announcement_id>/", views.admin_announcement_detail_view, name="admin_announcement_detail"),

    path("settings/", views.settings_view, name="admin_settings"),


    path("user-wallets/", views.user_wallets_view, name="user_wallets"),
    path("user/<int:user_id>/detail/", views.admin_user_detail_view, name="admin_user_detail"),
    path("user/<int:user_id>/adjust-wallet/", views.admin_adjust_wallet_view, name="admin_adjust_wallet"),


    path("admin/login/", views.admin_login_view, name="admin_login"),
    path("admin/logout/", views.admin_logout_view, name="admin_logout"),

    
]
