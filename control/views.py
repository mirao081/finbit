from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings as django_settings
import requests
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from accounts.models import (
    UserProfile,
    Wallet,
    Deposit,
    Withdrawal,
    Investment,
    Profit,
    Bonus,
    Referral,
    CompanyWallet,
    KYCSubmission,
    Announcement,
    AnnouncementReply,
    AssetPrice,
)

from core.models import InvestmentPlan, Investor, Transaction
from accounts.forms import DepositApprovalForm
from control.models import AdminDashboardSettings, AdminMenu


admin_required = user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url="admin_login",
)

from accounts.notifications import (
    notify_account_verified,
    notify_deposit_approved,
    notify_withdrawal_approved,
    notify_referral_bonus,
    notify_manual_referral_bonus,
)

@login_required
@admin_required
def dashboard_view(request):

    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()
    total_referrals = Referral.objects.count()

                                                               
                 
                                                               

    total_users = User.objects.count()

                                                               
                             
                                                               

    total_deposits = (
        Deposit.objects
        .filter(status="approved")
        .aggregate(
            total=Sum("amount_usd")
        )["total"]
        or Decimal("0.00")
    )

    total_deposits = total_deposits.quantize(
        Decimal("0.01")
    )

                                                               
                       
                                                               

    total_investments = (
        Investment.objects
        .filter(
            status__in=[
                "active",
                "completed",
            ]
        )
        .aggregate(
            total=Sum("amount_usd")
        )["total"]
        or Decimal("0.00")
    )

    total_investments = total_investments.quantize(
        Decimal("0.01")
    )

                                                               
                              
                                                               

    active_investments = (
        Investment.objects
        .filter(status="active")
        .count()
    )

                                                               
                                
                                                               

    total_withdrawals = (
        Withdrawal.objects
        .filter(status="approved")
        .aggregate(
            total=Sum("amount_usd")
        )["total"]
        or Decimal("0.00")
    )

    total_withdrawals = total_withdrawals.quantize(
        Decimal("0.01")
    )

                                                               
                            
                                                               

    investments_qs = (
        Investment.objects
        .filter(
            status__in=[
                "active",
                "completed",
            ]
        )
        .select_related(
            "user",
            "plan",
            "wallet",
        )
        .order_by("-created_at")
    )

    investments_page = Paginator(
        investments_qs,
        5,
    ).get_page(
        request.GET.get("investments_page")
    )

                                                               
                      
                                                               

    users_qs = (
        User.objects
        .order_by("-date_joined")
    )

    users_page = Paginator(
        users_qs,
        5,
    ).get_page(
        request.GET.get("users_page")
    )

                                                               
                                 
                                                               

    all_users_qs = (
        User.objects
        .select_related("userprofile")
        .order_by("-date_joined")
    )

    all_users_data = []

    for user in all_users_qs:

                                 
        referral = (
            Referral.objects
            .filter(referred_user=user)
            .select_related("user")
            .first()
        )

        wallets = (
            Wallet.objects
            .filter(user=user)
            .order_by("currency")
        )


        wallet_balance = Decimal("0.00")

        for wallet in wallets:

            available_asset = (
                wallet.balance
                - wallet.reserved_balance
            )

            if available_asset < Decimal("0"):
                available_asset = Decimal("0")

            asset_price = (
                AssetPrice.objects
                .filter(currency=wallet.currency)
                .first()
            )

            if not asset_price:
                continue

            exchange_rate = asset_price.usd_price

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):
                continue

            wallet_balance += (
                available_asset
                * exchange_rate
            )

        wallet_balance = wallet_balance.quantize(
            Decimal("0.01")
        )

                                                               
                                 
                                                               

        investment_total = (
            Investment.objects
            .filter(
                user=user,
                status="active",
            )
            .aggregate(
                total=Sum("amount_usd")
            )["total"]
            or Decimal("0.00")
        )

        investment_total = investment_total.quantize(
            Decimal("0.01")
        )

                                                               
                              
                                                               

        total_balance = wallet_balance

        all_users_data.append({
            "user": user,
            "profile": getattr(user, "userprofile", None),
            "referrer": referral.user if referral else None,
            "wallet_balance": wallet_balance,
            "investment_total": investment_total,
            "total_balance": total_balance,
    })
        
    all_users_page = Paginator(
        all_users_data,
        5,
    ).get_page(
        request.GET.get("all_users_page")
    )

                                                               
                       
                                                               

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    referral_queryset = (
        Referral.objects
        .select_related(
            "user",
            "referred_user",
        )
        .annotate(
            referrer_count=Count(
                "user__referrals",
                distinct=True,
            )
        )
        .order_by("-created_at")
    )

    if search_query:
        referral_queryset = referral_queryset.filter(
            Q(
                user__username__icontains=search_query
            )
            | Q(
                referred_user__username__icontains=search_query
            )
            | Q(
                user__email__icontains=search_query
            )
            | Q(
                referred_user__email__icontains=search_query
            )
        )

    referral_paginator = Paginator(
        referral_queryset,
        10,
    )

    referral_page = referral_paginator.get_page(
        request.GET.get("referral_page")
    )

                                                               
                     
                                                               

    activity_logs = []

                                                               
              
                                                               

    for deposit in (
        Deposit.objects
        .select_related(
            "user",
            "plan",
        )
        .order_by("-created_at")[:20]
    ):

        activity_logs.append({
            "type": "Deposit",
            "user": deposit.user,
            "amount": deposit.amount_usd,
            "asset_amount": (
                deposit.received_asset_amount
                or deposit.asset_amount
            ),
            "asset_code": deposit.payment_method,
            "status": deposit.status,
            "created_at": deposit.created_at,
        })

                                                               
                 
                                                               

    for withdrawal in (
        Withdrawal.objects
        .select_related(
            "user",
            "wallet",
        )
        .order_by("-created_at")[:20]
    ):

        activity_logs.append({
            "type": "Withdrawal",
            "user": withdrawal.user,
            "amount": withdrawal.amount_usd,
            "asset_amount": withdrawal.asset_amount,
            "asset_code": (
                withdrawal.wallet.currency
                if withdrawal.wallet
                else "—"
            ),
            "status": withdrawal.status,
            "created_at": withdrawal.created_at,
        })

                                                               
                 
                                                               

    for investment in (
        Investment.objects
        .select_related(
            "user",
            "plan",
            "wallet",
        )
        .order_by("-created_at")[:20]
    ):

        activity_logs.append({
            "type": "Investment",
            "user": investment.user,
            "amount": investment.amount_usd,
            "asset_amount": investment.asset_amount,
            "asset_code": (
                investment.wallet.currency
                if investment.wallet
                else "—"
            ),
            "status": investment.status,
            "created_at": investment.created_at,
        })

                                                               
                          
                                                               

    activity_logs = sorted(
        activity_logs,
        key=lambda item: item["created_at"],
        reverse=True,
    )

    activity_page = Paginator(
        activity_logs,
        5,
    ).get_page(
        request.GET.get("activity_page")
    )                                                               
                       
                                                               

    deposits_total = total_deposits
    withdrawals_total = total_withdrawals

    net_balance = (
        deposits_total
        - withdrawals_total
    ).quantize(
        Decimal("0.01")
    )

                                                               
                   
                                                               

    top_investors_qs = (
        User.objects
        .annotate(
            total_investment=Sum(
                "investments__amount_usd",
                filter=Q(
                    investments__status__in=[
                        "active",
                        "completed",
                    ]
                ),
            )
        )
        .filter(
            total_investment__isnull=False
        )
        .order_by(
            "-total_investment"
        )
    )

    top_investors_page = Paginator(
        top_investors_qs,
        5,
    ).get_page(
        request.GET.get("investors_page")
    )

                                                               
                                 
                                                               

    unread_replies_count = (
        AnnouncementReply.objects
        .filter(
            is_read_by_admin=False
        )
        .count()
    )

                                                               
             
                                                               

    context = {
        "settings": settings,
        "menus": menus,

                              
        "total_users": total_users,
        "total_deposits": total_deposits,
        "total_investments": total_investments,
        "active_investments": active_investments,
        "total_withdrawals": total_withdrawals,

                    
        "investments_page": investments_page,
        "users_page": users_page,
        "all_users_page": all_users_page,

                   
        "referral_page": referral_page,
        "search_query": search_query,

                  
        "activity_page": activity_page,

                           
        "deposits_total": deposits_total,
        "withdrawals_total": withdrawals_total,
        "net_balance": net_balance,

                       
        "top_investors_page": top_investors_page,

                             
        "unread_replies_count": unread_replies_count,
        "total_referrals": total_referrals,
    }

    return render(
        request,
        "control/dashboard.html",
        context,
    )

class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = [
            "name",
            "return_rate",
            "frequency",
            "duration",
            "total_return",
            "minimum_investment",
            "maximum_investment",
        ]


@admin_required
def investment_plans_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    plans = InvestmentPlan.objects.all().order_by("id")
    total_plans = plans.count()

    return render(
        request,
        "control/investment_plans.html",
        {
            "settings": settings,
            "menus": menus,
            "plans": plans,
            "total_plans": total_plans,
        },
    )


@admin_required
def update_plan_view(request, plan_id):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    plan = get_object_or_404(
        InvestmentPlan,
        id=plan_id,
    )

    if request.method == "POST":
        form = InvestmentPlanForm(
            request.POST,
            instance=plan,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Investment plan updated successfully.",
            )
            return redirect("investment_plans")
    else:
        form = InvestmentPlanForm(
            instance=plan,
        )

    return render(
        request,
        "control/update_plan.html",
        {
            "settings": settings,
            "menus": menus,
            "form": form,
            "plan": plan,
        },
    )


@admin_required
def records_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    records_qs = (
        Investment.objects
        .select_related("user", "plan")
        .order_by("-created_at")
    )

    paginator = Paginator(records_qs, 10)

    records_page = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/records.html",
        {
            "settings": settings,
            "menus": menus,
            "records_page": records_page,
        },
    )


class CompanyWalletForm(forms.ModelForm):
    class Meta:
        model = CompanyWallet
        fields = ["address", "qr_code"]


@admin_required
def payment_methods_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    wallets = CompanyWallet.objects.all()

    return render(
        request,
        "control/payment_methods.html",
        {
            "settings": settings,
            "menus": menus,
            "wallets": wallets,
        },
    )


@admin_required
def update_wallet_view(request, wallet_id):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    wallet = get_object_or_404(
        CompanyWallet,
        id=wallet_id,
    )

    if request.method == "POST":
        form = CompanyWalletForm(
            request.POST,
            request.FILES,
            instance=wallet,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Payment wallet updated successfully.",
            )
            return redirect("payment_methods")
    else:
        form = CompanyWalletForm(
            instance=wallet,
        )

    return render(
        request,
        "control/update_wallet.html",
        {
            "settings": settings,
            "menus": menus,
            "form": form,
            "wallet": wallet,
        },
    )


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["status"]


@admin_required
def deposits_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    deposits_qs = (
        Deposit.objects
        .select_related("user", "plan")
        .order_by("-created_at")
    )

    paginator = Paginator(
        deposits_qs,
        5,
    )

    deposits_page = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/deposits.html",
        {
            "settings": settings,
            "menus": menus,
            "deposits_page": deposits_page,
        },
    )





@login_required
@admin_required
def deposit_detail_view(request, deposit_id):

    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

                                                               
                  
                                                               

    deposit = (
        Deposit.objects
        .select_related(
            "user",
            "plan",
        )
        .filter(id=deposit_id)
        .first()
    )

    if not deposit:
        messages.error(
            request,
            "Deposit was not found.",
        )
        return redirect("deposits")

                                                               
                 
                                                               

    if request.method == "GET":

        form = DepositApprovalForm(
            instance=deposit,
        )

        return render(
            request,
            "control/deposit_detail.html",
            {
                "settings": settings,
                "menus": menus,
                "deposit": deposit,
                "form": form,
            },
        )

                                                               
                  
                                                               

    if request.method == "POST":

                                                          
                                
        referral = None
        referral_commission = Decimal("0.00")
        asset_amount = Decimal("0")
        wallet = None

                                                               
                                  
                                                               

        with transaction.atomic():

                                                               
                          
                                                               

            deposit = (
                Deposit.objects
                .select_for_update()
                .select_related(
                    "user",
                    "plan",
                )
                .filter(id=deposit_id)
                .first()
            )

            if not deposit:
                messages.error(
                    request,
                    "Deposit was not found.",
                )
                return redirect("deposits")

                                                               
                                          
                                                               

            if (
                deposit.status != "pending"
                or deposit.credited_to_wallet
            ):
                messages.warning(
                    request,
                    "This deposit has already been processed.",
                )
                return redirect("deposits")

                                                               
                          
                                                               

            form = DepositApprovalForm(
                request.POST,
                instance=deposit,
            )

            if not form.is_valid():

                return render(
                    request,
                    "control/deposit_detail.html",
                    {
                        "settings": settings,
                        "menus": menus,
                        "deposit": deposit,
                        "form": form,
                    },
                )

            new_status = form.cleaned_data.get("status")

                                                               
                            
                                                               

            if new_status == "rejected":

                deposit.status = "rejected"

                deposit.save(
                    update_fields=[
                        "status",
                    ],
                )

                messages.warning(
                    request,
                    "Deposit rejected successfully.",
                )

                return redirect("deposits")

                                                               
                             
                                                               

            if new_status != "approved":

                messages.error(
                    request,
                    "Invalid deposit status.",
                )

                return redirect("deposits")

                                                               
                                 
                                                               

            amount_usd = deposit.amount_usd

            if (
                amount_usd is None
                or not amount_usd.is_finite()
                or amount_usd <= Decimal("0")
            ):
                messages.error(
                    request,
                    "The deposit USD amount is invalid.",
                )
                return redirect("deposits")

                                                               
                              
                                                               

            wallet = (
                Wallet.objects
                .select_for_update()
                .filter(
                    user=deposit.user,
                    currency=deposit.payment_method,
                )
                .first()
            )

            if not wallet:

                messages.error(
                    request,
                    (
                        "The user's "
                        f"{deposit.get_payment_method_display()} "
                        "wallet was not found. "
                        "The deposit was not approved."
                    ),
                )

                return redirect("deposits")

                                                               
                                     
                                                               

            asset_price = (
                AssetPrice.objects
                .filter(
                    currency=deposit.payment_method,
                )
                .first()
            )

            if not asset_price:

                messages.error(
                    request,
                    (
                        "No USD exchange rate has been configured "
                        f"for {deposit.get_payment_method_display()}."
                    ),
                )

                return redirect("deposits")

            exchange_rate = asset_price.usd_price

                                                               
                                    
                                                               

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):

                messages.error(
                    request,
                    "The asset exchange rate is invalid.",
                )

                return redirect("deposits")

                                                               
                                     
                                                               
             
                                                  
             
                      
             
                            
             
                                  
             
                                                               

            asset_amount = (
                amount_usd / exchange_rate
            ).quantize(
                Decimal("0.000000000001")
            )

                                                               
                                        
                                                               

            if (
                not asset_amount.is_finite()
                or asset_amount <= Decimal("0")
            ):

                messages.error(
                    request,
                    "The calculated asset amount is invalid.",
                )

                return redirect("deposits")

                                                               
                                 
                                                               

            usd_value = (
                asset_amount * exchange_rate
            ).quantize(
                Decimal("0.01")
            )

                                                               
                                
                                                               

            wallet.balance += asset_amount

            wallet.save(
                update_fields=[
                    "balance",
                    "updated_at",
                ],
            )

                                                               
                                   
                                                               

            investor, _ = (
                Investor.objects
                .get_or_create(
                    user=deposit.user,
                    defaults={
                        "name": deposit.user.username,
                    },
                )
            )

                                                               
                                
                                                               

            Transaction.objects.create(
                investor=investor,
                wallet=wallet,
                transaction_type="deposit",
                direction="credit",
                asset_amount=asset_amount,
                usd_value=usd_value,
                exchange_rate=exchange_rate,
                reference=f"DEP-{deposit.id}",
                description=(
                    "Deposit credited to "
                    f"{wallet.get_currency_display()} wallet"
                ),
            )

                                                               
                                           
                                                               
             
                                                       
                                                
             
                            
                                    
             
                                  
                                  
             
                                        
             
                                                               

            referral = (
                Referral.objects
                .select_for_update()
                .filter(
                    referred_user=deposit.user,
                )
                .first()
            )

            referral_commission = Decimal("0.00")

            if referral:

                referral_commission = (
                    amount_usd * Decimal("0.084")
                ).quantize(
                    Decimal("0.01")
                )

                if referral_commission > Decimal("0"):

                    referral.commission_earned += (
                        referral_commission
                    )

                    referral.save(
                        update_fields=[
                            "commission_earned",
                        ],
                    )

                                                               
                            
                                                               

            deposit.asset_amount = asset_amount
            deposit.received_asset_amount = asset_amount
            deposit.exchange_rate = exchange_rate
            deposit.status = "approved"
            deposit.credited_to_wallet = True
            deposit.approved_at = timezone.now()

            deposit.save(
                update_fields=[
                    "asset_amount",
                    "received_asset_amount",
                    "exchange_rate",
                    "status",
                    "credited_to_wallet",
                    "approved_at",
                ],
            )

                                                               
                            
                                                               
         
                                                               
         
                                                         
                                                                
                                                                 
                                  
         
                                   
                                    
                                   
         
                                 
                                    
                                   
         
                                                               

        notify_deposit_approved(
            deposit
        )

        if (
            referral
            and referral_commission > Decimal("0")
        ):

            notify_referral_bonus(
                referral,
                referral_commission,
            )

                                                               
                         
                                                               

        if (
            referral
            and referral_commission > Decimal("0")
        ):

            messages.success(
                request,
                (
                    "Deposit approved successfully. "
                    f"{asset_amount} "
                    f"{wallet.get_currency_display()} "
                    "has been credited to the user's wallet. "
                    f"A ${referral_commission:.2f} referral "
                    "commission was automatically credited "
                    f"to {referral.user.username}."
                ),
            )

        else:

            messages.success(
                request,
                (
                    "Deposit approved successfully. "
                    f"{asset_amount} "
                    f"{wallet.get_currency_display()} "
                    "has been credited to the user's wallet."
                ),
            )

        return redirect("deposits")

                                                               
                    
                                                               

    messages.error(
        request,
        "Invalid request method.",
    )

    return redirect("deposits")



def investments_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    investments_qs = (
        Investment.objects
        .all()
        .order_by("-created_at")
    )

    paginator = Paginator(
        investments_qs,
        5,
    )

    investments_page = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/investments.html",
        {
            "settings": settings,
            "menus": menus,
            "investments_page": investments_page,
        },
    )


@admin_required
def all_transactions_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    transactions_qs = (
        Transaction.objects
        .all()
        .order_by("-date")
    )

    paginator = Paginator(
        transactions_qs,
        5,
    )

    transactions_page = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/all_transactions.html",
        {
            "transactions_page": transactions_page,
            "settings": settings,
            "menus": menus,
        },
    )


@admin_required
def user_verifications_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    submissions = (
        KYCSubmission.objects
        .select_related("user")
        .order_by("-uploaded_at")
    )

    return render(
        request,
        "control/user_verifications.html",
        {
            "settings": settings,
            "menus": menus,
            "submissions": submissions,
        },
    )


@admin_required
@require_POST
def approve_kyc(request, submission_id):

    notification_needed = False

    with transaction.atomic():

                                                               
                                      
                                                               

        submission = (
            KYCSubmission.objects
            .select_for_update()
            .select_related("user")
            .filter(id=submission_id)
            .first()
        )

        if not submission:

            messages.error(
                request,
                "KYC submission was not found.",
            )

            return redirect(
                "user_verifications"
            )

                                                               
                                   
                                                               

        profile, created = (
            UserProfile.objects
            .get_or_create(
                user=submission.user,
            )
        )

                                                          
        was_verified = profile.kyc_verified

                                                               
                     
                                                               

        submission.approved = True

        submission.save(
            update_fields=[
                "approved",
            ]
        )

                                                               
                             
                                                               

        profile.kyc_verified = True

        profile.save(
            update_fields=[
                "kyc_verified",
            ]
        )

                                                               
                                                        
                          
                                                               

        if not was_verified:
            notification_needed = True

                                                               
                                                          
                                                               

    if notification_needed:

        notify_account_verified(
            submission.user
        )

                                                               
                           
                                                               

    messages.success(
        request,
        f"KYC for {submission.user.username} approved.",
    )

    return redirect(
        "user_verifications"
    )

@admin_required
@require_POST
def reject_kyc(request, submission_id):
    with transaction.atomic():
        submission = (
            KYCSubmission.objects
            .select_for_update()
            .select_related("user")
            .filter(id=submission_id)
            .first()
        )

        if not submission:
            messages.error(
                request,
                "KYC submission was not found.",
            )
            return redirect("user_verifications")

        submission.approved = False
        submission.save(
            update_fields=["approved"]
        )

        profile, created = (
            UserProfile.objects
            .get_or_create(
                user=submission.user
            )
        )

        profile.kyc_verified = False
        profile.save(
            update_fields=["kyc_verified"]
        )

    messages.warning(
        request,
        f"KYC for {submission.user.username} rejected.",
    )

    return redirect("user_verifications")


@admin_required
def kyc_detail_view(request, submission_id):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    submission = get_object_or_404(
        KYCSubmission,
        id=submission_id,
    )

    file_url = (
        submission.document.url
        if submission.document
        else ""
    )

    file_type = ""

    if file_url.lower().endswith(".pdf"):
        file_type = "pdf"
    elif file_url.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        file_type = "image"
    else:
        file_type = "other"

    return render(
        request,
        "control/kyc_detail.html",
        {
            "settings": settings,
            "menus": menus,
            "submission": submission,
            "file_type": file_type,
        },
    )


@login_required
@admin_required
def user_wallets_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    users_qs = (
        User.objects
        .select_related("userprofile")
        .order_by("-date_joined")
    )

    wallet_data = []

    for u in users_qs:
                                                                   
                      
                                                                   

        wallets = (
            Wallet.objects
            .filter(user=u)
            .order_by("currency")
        )

                                                                   
                                             
                                                                   
         
                                                           
                                                      
                                                 
                                                                   

        wallet_balance = Decimal("0.00")

        for wallet in wallets:
            available_asset = (
                wallet.balance
                - wallet.reserved_balance
            )

            if available_asset < Decimal("0"):
                available_asset = Decimal("0")

            asset_price = (
                AssetPrice.objects
                .filter(currency=wallet.currency)
                .first()
            )

            if not asset_price:
                continue

            exchange_rate = asset_price.usd_price

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):
                continue

            wallet_balance += (
                available_asset * exchange_rate
            )

        wallet_balance = wallet_balance.quantize(
            Decimal("0.01")
        )

                                                                   
                                
                                                                   
         
                                                              
                                                            
                            
                                                                   

        wallet = wallets.first()

        wallet_address = (
            wallet.address
            if wallet and wallet.address
            else "N/A"
        )

                                                                   
                           
                                                                   

        deposits_total = (
            Deposit.objects
            .filter(
                user=u,
                status="approved",
            )
            .aggregate(
                total=Sum("amount_usd")
            )["total"]
            or Decimal("0.00")
        )

        deposits_total = deposits_total.quantize(
            Decimal("0.01")
        )

                                                                   
                              
                                                                   

        withdrawals_total = (
            Withdrawal.objects
            .filter(
                user=u,
                status="approved",
            )
            .aggregate(
                total=Sum("amount_usd")
            )["total"]
            or Decimal("0.00")
        )

        withdrawals_total = withdrawals_total.quantize(
            Decimal("0.01")
        )

                                                                   
                     
                                                                   

        investments_total = (
            Investment.objects
            .filter(user=u)
            .aggregate(
                total=Sum("amount_usd")
            )["total"]
            or Decimal("0.00")
        )

        investments_total = investments_total.quantize(
            Decimal("0.01")
        )

                                                                   
                          
                                                                   

        profits_total = (
            Profit.objects
            .filter(
                user=u,
                status="approved",
            )
            .aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        profits_total = profits_total.quantize(
            Decimal("0.01")
        )

                                                                   
                          
                                                                   

        bonuses_total = (
            Bonus.objects
            .filter(
                user=u,
                status="approved",
            )
            .aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        bonuses_total = bonuses_total.quantize(
            Decimal("0.01")
        )

                                                                   
                               
                                                                   
         
                                                                
                              
         
                                                               
                                                                
                                                         
                                                                   

        net_balance = wallet_balance

                                                                   
                         
                                                                   

        recent_deposits = (
            Deposit.objects
            .filter(user=u)
            .select_related("plan")
            .order_by("-created_at")[:5]
        )

                                                                   
                            
                                                                   

        recent_withdrawals = (
            Withdrawal.objects
            .filter(user=u)
            .select_related("wallet")
            .order_by("-created_at")[:5]
        )

                                                                   
                     
                                                                   

        wallet_data.append({
            "user": u,
            "profile": getattr(
                u,
                "userprofile",
                None,
            ),

            "wallets": wallets,

            "wallet_balance": wallet_balance,
            "wallet_address": wallet_address,

            "deposits_total": deposits_total,
            "withdrawals_total": withdrawals_total,
            "investments_total": investments_total,
            "profits_total": profits_total,
            "bonuses_total": bonuses_total,

            "net_balance": net_balance,

            "recent_deposits": recent_deposits,
            "recent_withdrawals": recent_withdrawals,
        })

                                                                   
                
                                                                   

    page_obj = Paginator(
        wallet_data,
        10,
    ).get_page(
        request.GET.get("page")
    )

                                                                   
             
                                                                   

    context = {
        "settings": settings,
        "menus": menus,
        "page_obj": page_obj,
    }

    return render(
        request,
        "control/user_wallets.html",
        context,
    )


@admin_required
def admin_user_detail_view(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
    )

    profile = getattr(
        user,
        "userprofile",
        None,
    )

    wallet = (
        Wallet.objects
        .filter(user=user)
        .first()
    )

    wallet_balance = (
        wallet.balance
        if wallet
        else Decimal("0.00")
    )

    wallet_address = (
        wallet.address
        if wallet and hasattr(wallet, "address")
        else "N/A"
    )

    recent_deposits = (
        Deposit.objects
        .filter(user=user)
        .order_by("-created_at")[:5]
    )

    recent_withdrawals = (
        Withdrawal.objects
        .filter(user=user)
        .order_by("-created_at")[:5]
    )

    context = {
        "user": user,
        "profile": profile,
        "wallet_balance": wallet_balance,
        "wallet_address": wallet_address,
        "recent_deposits": recent_deposits,
        "recent_withdrawals": recent_withdrawals,
    }

    return render(
        request,
        "control/admin_user_detail.html",
        context,
    )


@admin_required
@require_POST
def admin_adjust_wallet_view(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id,
    )

    amount_raw = request.POST.get(
        "amount",
        "0.00",
    )

    action = request.POST.get("action")

    try:
        amount = Decimal(amount_raw)
    except (InvalidOperation, TypeError, ValueError):
        messages.error(
            request,
            "Invalid amount.",
        )
        return redirect("user_wallets")

    if not amount.is_finite():
        messages.error(
            request,
            "Invalid amount.",
        )
        return redirect("user_wallets")

    if amount <= Decimal("0.00"):
        messages.error(
            request,
            "Amount must be greater than zero.",
        )
        return redirect("user_wallets")

    with transaction.atomic():
        wallet = (
            Wallet.objects
            .select_for_update()
            .filter(user=user)
            .first()
        )

        if not wallet:
            messages.error(
                request,
                "User wallet was not found.",
            )
            return redirect("user_wallets")

        if action == "credit":
            wallet.balance += amount

        elif action == "debit":
            if wallet.balance < amount:
                messages.error(
                    request,
                    "Insufficient wallet balance.",
                )
                return redirect("user_wallets")

            wallet.balance -= amount

        else:
            messages.error(
                request,
                "Invalid wallet action.",
            )
            return redirect("user_wallets")

        wallet.save(
            update_fields=["balance"]
        )

    messages.success(
        request,
        f"Wallet updated for {user.username}.",
    )

    return redirect("user_wallets")


@admin_required
def admin_announcements_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    announcements_list = (
        Announcement.objects
        .order_by("-created_at")
    )

    paginator = Paginator(
        announcements_list,
        5,
    )

    announcements = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/admin_announcements.html",
        {
            "settings": settings,
            "menus": menus,
            "announcements": announcements,
        },
    )


@admin_required
@require_POST
def admin_announcement_detail_view(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
    )

    message = request.POST.get(
        "message",
        "",
    ).strip()

    if message:
        users = User.objects.all()

        AnnouncementReply.objects.bulk_create([
            AnnouncementReply(
                announcement=announcement,
                user=target_user,
                message=message,
                is_read_by_user=False,
                is_read_by_admin=True,
            )
            for target_user in users
        ])

    return redirect(
        "admin_announcement_detail",
        announcement_id=announcement.id,
    )




@login_required
@admin_required
def settings_view(request):

                                                               
                          
                                                               
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        current_page = request.POST.get("page", "1")

        if action and user_id:
            target_user = get_object_or_404(
                User,
                id=user_id,
            )

                                                               
                    
                                                               
            try:
                amount_usd = Decimal(
                    request.POST.get("amount") or "0"
                )
            except (
                InvalidOperation,
                TypeError,
                ValueError,
            ):
                amount_usd = Decimal("0")

            if not amount_usd.is_finite():
                messages.error(
                    request,
                    "Invalid amount.",
                )
                return redirect(
                    f"/admin/settings/?page={current_page}"
                )

                                                               
                     
                                                               
            message = request.POST.get(
                "message",
                "",
            ).strip()

                                                               
                                   
                                                               
            if amount_usd < Decimal("0"):
                messages.error(
                    request,
                    "Amount cannot be negative.",
                )
                return redirect(
                    f"/admin/settings/?page={current_page}"
                )

            amount_usd = amount_usd.quantize(
                Decimal("0.01")
            )

                                                               
                        
                                                               
            if action == "fund":

                if amount_usd <= Decimal("0"):
                    messages.error(
                        request,
                        "Funding amount must be greater than zero.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                wallet_currency = request.POST.get(
                    "wallet_currency"
                )

                allowed_wallets = {
                    "BTC",
                    "ETH",
                    "USDT_TRC20",
                    "USDT_ERC20",
                }

                if wallet_currency not in allowed_wallets:
                    messages.error(
                        request,
                        "Please select a valid wallet.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                with transaction.atomic():

                    wallet = (
                        Wallet.objects
                        .select_for_update()
                        .filter(
                            user=target_user,
                            currency=wallet_currency,
                        )
                        .first()
                    )

                    if not wallet:
                        messages.error(
                            request,
                            "The selected user wallet was not found.",
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                   
                                                               
                    asset_price = (
                        AssetPrice.objects
                        .filter(
                            currency=wallet.currency
                        )
                        .first()
                    )

                    if not asset_price:
                        messages.error(
                            request,
                            (
                                "No exchange rate is configured "
                                f"for {wallet.get_currency_display()}."
                            ),
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                    exchange_rate = asset_price.usd_price

                    if (
                        exchange_rate is None
                        or not exchange_rate.is_finite()
                        or exchange_rate <= Decimal("0")
                    ):
                        messages.error(
                            request,
                            "The wallet exchange rate is invalid.",
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                                 
                                                               
                    asset_amount = (
                        amount_usd / exchange_rate
                    ).quantize(
                        Decimal("0.000000000001")
                    )

                    if asset_amount <= Decimal("0"):
                        messages.error(
                            request,
                            "The calculated asset amount is invalid.",
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                   
                                                               
                    wallet.balance += asset_amount

                    wallet.save(
                        update_fields=[
                            "balance",
                            "updated_at",
                        ]
                    )

                                                               
                                           
                                                               
                    investor, _ = (
                        Investor.objects
                        .get_or_create(
                            user=target_user,
                            defaults={
                                "name": target_user.username,
                            },
                        )
                    )

                                                               
                                        
                                                               
                    Transaction.objects.create(
                        investor=investor,
                        wallet=wallet,
                        transaction_type="admin_credit",
                        direction="credit",
                        asset_amount=asset_amount,
                        usd_value=amount_usd,
                        exchange_rate=exchange_rate,
                        reference=(
                            f"ADMIN-CREDIT-{target_user.id}"
                        ),
                        description=(
                            "Admin credited wallet"
                        ),
                    )

                messages.success(
                    request,
                    (
                        f"${amount_usd} was credited to "
                        f"{target_user.username}'s "
                        f"{wallet.get_currency_display()} wallet."
                    ),
                )

                                                               
                          
                                                               
            elif action == "deduct":

                if amount_usd <= Decimal("0"):
                    messages.error(
                        request,
                        "Deduction amount must be greater than zero.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                wallet_currency = request.POST.get(
                    "wallet_currency"
                )

                allowed_wallets = {
                    "BTC",
                    "ETH",
                    "USDT_TRC20",
                    "USDT_ERC20",
                }

                if wallet_currency not in allowed_wallets:
                    messages.error(
                        request,
                        "Please select a valid wallet.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                with transaction.atomic():

                    wallet = (
                        Wallet.objects
                        .select_for_update()
                        .filter(
                            user=target_user,
                            currency=wallet_currency,
                        )
                        .first()
                    )

                    if not wallet:
                        messages.error(
                            request,
                            "The selected user wallet was not found.",
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                   
                                                               
                    asset_price = (
                        AssetPrice.objects
                        .filter(
                            currency=wallet.currency
                        )
                        .first()
                    )

                    if not asset_price:
                        messages.error(
                            request,
                            (
                                "No exchange rate is configured "
                                f"for {wallet.get_currency_display()}."
                            ),
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                    exchange_rate = asset_price.usd_price

                    if (
                        exchange_rate is None
                        or not exchange_rate.is_finite()
                        or exchange_rate <= Decimal("0")
                    ):
                        messages.error(
                            request,
                            "The wallet exchange rate is invalid.",
                        )
                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                          
                                                               
                    asset_amount = (
                        amount_usd / exchange_rate
                    ).quantize(
                        Decimal("0.000000000001")
                    )

                                                               
                                              
                                                               
                    available_wallet_asset = (
                        wallet.balance
                        - wallet.reserved_balance
                    )

                    if available_wallet_asset < Decimal("0"):
                        available_wallet_asset = Decimal("0")

                                                               
                                              
                                                               
                    if asset_amount > available_wallet_asset:

                        available_usd = (
                            available_wallet_asset
                            * exchange_rate
                        ).quantize(
                            Decimal("0.01")
                        )

                        messages.error(
                            request,
                            (
                                f"Insufficient available "
                                f"{wallet.get_currency_display()} "
                                f"balance. Only approximately "
                                f"${available_usd} is available."
                            ),
                        )

                        return redirect(
                            f"/admin/settings/?page={current_page}"
                        )

                                                               
                                        
                                                               
                    wallet.balance -= asset_amount

                    wallet.save(
                        update_fields=[
                            "balance",
                            "updated_at",
                        ]
                    )

                                                               
                                           
                                                               
                    investor, _ = (
                        Investor.objects
                        .get_or_create(
                            user=target_user,
                            defaults={
                                "name": target_user.username,
                            },
                        )
                    )

                                                               
                                        
                                                               
                    Transaction.objects.create(
                        investor=investor,
                        wallet=wallet,
                        transaction_type="admin_debit",
                        direction="debit",
                        asset_amount=asset_amount,
                        usd_value=amount_usd,
                        exchange_rate=exchange_rate,
                        reference=(
                            f"ADMIN-DEBIT-{target_user.id}"
                        ),
                        description=(
                            "Admin deducted from wallet"
                        ),
                    )

                messages.success(
                    request,
                    (
                        f"${amount_usd} was deducted from "
                        f"{target_user.username}'s "
                        f"{wallet.get_currency_display()} wallet."
                    ),
                )

                                                               
                        
                                                               
            elif action == "add_profit":

                if amount_usd <= Decimal("0"):
                    messages.error(
                        request,
                        "Profit amount must be greater than zero.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                plan_id = request.POST.get("plan_id")

                if not plan_id:
                    messages.error(
                        request,
                        "Please select an investment plan.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                selected_plan = get_object_or_404(
                    InvestmentPlan,
                    id=plan_id,
                )

                                                               
                                                            
                                                               
                has_investment = Investment.objects.filter(
                    user=target_user,
                    plan=selected_plan,
                    status="active",
                ).exists()

                if not has_investment:
                    messages.error(
                        request,
                        (
                            f"{target_user.username} does not have "
                            f"an active investment in "
                            f"{selected_plan.name}."
                        ),
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                                                               
                                        
                                                               
                Profit.objects.create(
                    user=target_user,
                    plan=selected_plan,
                    amount=amount_usd,
                    status="approved",
                )

                messages.success(
                    request,
                    (
                        f"${amount_usd} profit was added to "
                        f"{target_user.username}'s "
                        f"{selected_plan.name} investment."
                    ),
                )

                                                               
                              
                                                               
            elif action == "referral_bonus":

                if amount_usd <= Decimal("0"):
                    messages.error(
                        request,
                        "Bonus amount must be greater than zero.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                                                                   
                                                             
                             
                 
                                                               
                                                                
                              
                                                                   
                Bonus.objects.create(
                    user=target_user,
                    amount=amount_usd,
                    bonus_type="manual",
                    status="approved",
                    description="Referral bonus",
                )

                messages.success(
                    request,
                    (
                        f"${amount_usd} referral bonus was added "
                        f"to {target_user.username}'s account."
                    ),
                )

                                                               
                        
                                                               
            elif action == "send_email":

                if message and target_user.email:

                    send_mail(
                        subject="Message from Admin",
                        message=message,
                        from_email=django_settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[
                            target_user.email
                        ],
                        fail_silently=False,
                    )

                    messages.success(
                        request,
                        "Message sent successfully.",
                    )

                else:

                    messages.error(
                        request,
                        "Please provide a message and make sure the user has an email address.",
                    )

                                                               
                           
                                                               
            elif action == "login_as_user":

                                                           
                request.session["admin_user_id"] = (
                    request.user.id
                )

                                             
                login(
                    request,
                    target_user,
                    backend=(
                        "django.contrib.auth.backends.ModelBackend"
                    ),
                )

                return redirect("dashboard")

                                                               
                         
                                                               
            elif action == "delete_user":

                if target_user.id == request.user.id:
                    messages.error(
                        request,
                        "You cannot delete your own admin account.",
                    )
                    return redirect(
                        f"/admin/settings/?page={current_page}"
                    )

                target_user.delete()

                messages.success(
                    request,
                    "User deleted successfully.",
                )

                                                               
                            
                                                               
            else:

                messages.error(
                    request,
                    "Invalid admin action.",
                )

            return redirect(
                f"{reverse('admin_settings')}?page={current_page}"
            )

                                                               
                         
                                                               
    dashboard_settings = (
        AdminDashboardSettings.objects.first()
    )

    menus = AdminMenu.objects.all()

                                                               
           
                                                               
    users = (
        User.objects
        .all()
        .order_by("-date_joined")
    )

                                                               
                
                                                               
    paginator = Paginator(
        users,
        6,
    )

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )

                                                               
               
                                                               
    user_data = []

    for user in page_obj.object_list:

                                                               
                      
                                                               
        wallets = (
            Wallet.objects
            .filter(user=user)
            .order_by("currency")
        )

                                                               
                               
         
                                                          
                                                               
        investment_plans = (
            InvestmentPlan.objects
            .all()
            .order_by("name")
        )

                                                               
                                               
                                                               
        wallet_balance = Decimal("0.00")

        for wallet in wallets:

            available_asset = (
                wallet.balance
                - wallet.reserved_balance
            )

            if available_asset < Decimal("0"):
                available_asset = Decimal("0")

                                                             
                                 
                                                             
            asset_price = (
                AssetPrice.objects
                .filter(
                    currency=wallet.currency
                )
                .first()
            )

            if not asset_price:
                continue

            exchange_rate = asset_price.usd_price

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):
                continue

                                                             
                                  
                                                             
            wallet_usd_value = (
                available_asset
                * exchange_rate
            )

            wallet_balance += wallet_usd_value

        wallet_balance = wallet_balance.quantize(
            Decimal("0.01")
        )

                                                               
                           
                                                               
        available_balance = wallet_balance

                                                               
                            
                                                               
        active_investments = (
            Investment.objects
            .filter(
                user=user,
                status="active",
            )
            .aggregate(
                total=Sum("amount_usd")
            )["total"]
            or Decimal("0.00")
        )

        active_investments = active_investments.quantize(
            Decimal("0.01")
        )

                                                               
                          
                                                               
        profit_total = (
            Profit.objects
            .filter(
                user=user,
                status="approved",
            )
            .aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        profit_total = profit_total.quantize(
            Decimal("0.01")
        )

                                                               
                          
                                                               
        bonus_total = (
            Bonus.objects
            .filter(
                user=user,
                status="approved",
            )
            .aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        bonus_total = bonus_total.quantize(
            Decimal("0.01")
        )

                                                               
                      
                                                               
        total_earned = (
            profit_total
            + bonus_total
        ).quantize(
            Decimal("0.01")
        )

                                                               
                               
         
                                            
                                                               
        total_portfolio = (
            wallet_balance
            + active_investments
            + profit_total
            + bonus_total
        ).quantize(
            Decimal("0.01")
        )

                                                               
                         
                                                               
        user_data.append({
            "user": user,
            "wallets": wallets,

            "investment_plans": investment_plans,

            "wallet_balance": wallet_balance,
            "available_balance": available_balance,
            "active_investments": active_investments,
            "profit_total": profit_total,
            "bonus_total": bonus_total,
            "total_earned": total_earned,
            "total_portfolio": total_portfolio,
        })

                                                               
                           
                                                               
    return render(
        request,
        "control/admin_settings.html",
        {
            "user_data": user_data,
            "page_obj": page_obj,
            "settings": dashboard_settings,
            "menus": menus,
        },
    )


@admin_required
def withdrawals_view(request):
    settings = AdminDashboardSettings.objects.first()
    menus = AdminMenu.objects.all()

    withdrawals_qs = (
        Withdrawal.objects
        .all()
        .order_by("-created_at")
    )

    paginator = Paginator(
        withdrawals_qs,
        5,
    )

    withdrawals_page = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "control/withdrawals.html",
        {
            "settings": settings,
            "menus": menus,
            "withdrawals_page": withdrawals_page,
        },
    )


@login_required
@admin_required
@require_POST
def approve_withdrawal(request, withdrawal_id):

                                                               
                        
                                                               

    with transaction.atomic():

        withdrawal = (
            Withdrawal.objects
            .select_for_update()
            .select_related(
                "user",
                "wallet",
            )
            .filter(
                id=withdrawal_id,
                status="pending",
            )
            .first()
        )

                                                               
                          
                                                               

        if withdrawal is None:

            messages.error(
                request,
                "Withdrawal was not found or has already been processed.",
            )

            return redirect(
                "withdrawals"
            )

                                                               
                             
                                                               

        amount_usd = withdrawal.amount_usd

        if (
            amount_usd is None
            or not amount_usd.is_finite()
            or amount_usd <= Decimal("0.00")
        ):

            messages.error(
                request,
                "Invalid withdrawal USD amount.",
            )

            return redirect(
                "withdrawals"
            )

                                                               
                          
                                                               

        wallet = (
            Wallet.objects
            .select_for_update()
            .filter(
                id=withdrawal.wallet_id,
                user=withdrawal.user,
            )
            .first()
        )

        if wallet is None:

            messages.error(
                request,
                "The wallet for this withdrawal was not found.",
            )

            return redirect(
                "withdrawals"
            )

                                                               
                                     
                                                               

        destination = (
            withdrawal.destination_wallet or ""
        ).strip()

        if not destination:

            messages.error(
                request,
                "The withdrawal destination wallet is missing.",
            )

            return redirect(
                "withdrawals"
            )

        if not wallet.address:

            messages.error(
                request,
                "The user's wallet address is missing.",
            )

            return redirect(
                "withdrawals"
            )

        if destination != wallet.address.strip():

            messages.error(
                request,
                (
                    "The withdrawal destination does not "
                    "match the user's saved wallet address."
                ),
            )

            return redirect(
                "withdrawals"
            )

                                                               
                                                   
                                                               

        asset_amount = withdrawal.asset_amount
        exchange_rate = withdrawal.exchange_rate

                                                               
                                                      
                                                               

        if (
            asset_amount is None
            or not asset_amount.is_finite()
            or asset_amount <= Decimal("0")
        ):

            asset_price = (
                AssetPrice.objects
                .filter(
                    currency=wallet.currency,
                )
                .first()
            )

            if asset_price is None:

                messages.error(
                    request,
                    (
                        "No USD exchange rate has been configured "
                        f"for {wallet.get_currency_display()}."
                    ),
                )

                return redirect(
                    "withdrawals"
                )

            exchange_rate = asset_price.usd_price

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):

                messages.error(
                    request,
                    "The exchange rate for this withdrawal is invalid.",
                )

                return redirect(
                    "withdrawals"
                )

            asset_amount = (
                amount_usd / exchange_rate
            ).quantize(
                Decimal("0.000000000001")
            )

            if asset_amount <= Decimal("0"):

                messages.error(
                    request,
                    "The calculated withdrawal asset amount is invalid.",
                )

                return redirect(
                    "withdrawals"
                )

        else:

                                                               
                                              
                                                               

            if (
                exchange_rate is None
                or not exchange_rate.is_finite()
                or exchange_rate <= Decimal("0")
            ):

                exchange_rate = (
                    amount_usd / asset_amount
                ).quantize(
                    Decimal("0.000000000001")
                )

                                                               
                             
                                                               

        wallet_balance = (
            wallet.balance
            or Decimal("0")
        )

        reserved_balance = (
            wallet.reserved_balance
            or Decimal("0")
        )

        if wallet_balance < Decimal("0"):
            wallet_balance = Decimal("0")

        if reserved_balance < Decimal("0"):
            reserved_balance = Decimal("0")

        available_balance = (
            wallet_balance
            - reserved_balance
        )

        if available_balance < Decimal("0"):
            available_balance = Decimal("0")

                                                               
                                 
                                                               

        if asset_amount > available_balance:

            available_usd = (
                available_balance * exchange_rate
            ).quantize(
                Decimal("0.01")
            )

            messages.error(
                request,
                (
                    f"Insufficient available "
                    f"{wallet.get_currency_display()} balance. "
                    f"The withdrawal requires {asset_amount} "
                    f"{wallet.currency}, worth ${amount_usd}, "
                    f"but only {available_balance} "
                    f"{wallet.currency}, worth ${available_usd}, "
                    f"is available."
                ),
            )

            return redirect(
                "withdrawals"
            )

                                                               
                                  
                                                               

        wallet.balance = (
            wallet_balance
            - asset_amount
        )

                                                               
                                 
                                                               

        if reserved_balance >= asset_amount:

            wallet.reserved_balance = (
                reserved_balance
                - asset_amount
            )

        else:

            wallet.reserved_balance = Decimal("0")

        wallet.save(
            update_fields=[
                "balance",
                "reserved_balance",
                "updated_at",
            ]
        )

                                                               
                           
                                                               

        withdrawal.asset_amount = asset_amount
        withdrawal.exchange_rate = exchange_rate
        withdrawal.status = "approved"
        withdrawal.approved_at = timezone.now()

        withdrawal.save(
            update_fields=[
                "asset_amount",
                "exchange_rate",
                "status",
                "approved_at",
            ]
        )

                                                               
                               
                                                               

        investor, _ = (
            Investor.objects
            .get_or_create(
                user=withdrawal.user,
                defaults={
                    "name": withdrawal.user.username,
                },
            )
        )

                                                               
                            
                                                               

        Transaction.objects.create(
            investor=investor,
            wallet=wallet,
            transaction_type="withdrawal",
            direction="debit",
            asset_amount=asset_amount,
            usd_value=amount_usd,
            exchange_rate=exchange_rate,
            reference=f"WDR-{withdrawal.id}",
            description=(
                f"Withdrawal to {destination}"
            ),
        )

                                                               
                                           
                                                               
     
                                                              
                                                           
                                                      
     
                 
     
                            
                           
     
                                                               

    notify_withdrawal_approved(
        withdrawal
    )

                                                               
                           
                                                               

    messages.success(
        request,
        "Withdrawal approved successfully.",
    )

    return redirect(
        "withdrawals"
    )


@login_required
@admin_required
@require_POST
def reject_withdrawal(request, withdrawal_id):
    with transaction.atomic():

        withdrawal = (
            Withdrawal.objects
            .select_for_update()
            .select_related("user", "wallet")
            .filter(
                id=withdrawal_id,
                status="pending",
            )
            .first()
        )

        if withdrawal is None:
            messages.error(
                request,
                "Withdrawal was not found or has already been processed."
            )
            return redirect("withdrawals")

        wallet = (
            Wallet.objects
            .select_for_update()
            .filter(
                id=withdrawal.wallet_id,
                user=withdrawal.user,
            )
            .first()
        )

        if wallet is not None:

            reserved_balance = (
                wallet.reserved_balance or Decimal("0")
            )

            release_amount = (
                withdrawal.asset_amount
                or Decimal("0")
            )

            if release_amount > Decimal("0"):

                wallet.reserved_balance = max(
                    Decimal("0"),
                    reserved_balance - release_amount,
                )

                wallet.save(
                    update_fields=[
                        "reserved_balance",
                        "updated_at",
                    ]
                )

        withdrawal.status = "rejected"

        withdrawal.save(
            update_fields=[
                "status",
            ]
        )

    messages.success(
        request,
        "Withdrawal rejected successfully."
    )

    return redirect("withdrawals")


def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get(
            "username",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        recaptcha_response = request.POST.get(
            "g-recaptcha-response",
            "",
        )

        ip_address = request.META.get(
            "REMOTE_ADDR",
            "unknown",
        )

        rate_limit_key = (
            f"admin_login_attempts:{ip_address}:{username.lower()}"
        )

        attempts = cache.get(
            rate_limit_key,
            0,
        )

        if attempts >= 3:
            messages.error(
                request,
                "Too many failed login attempts. Please try again later."
            )

            return render(
                request,
                "control/admin_login.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
                },
            )

        if not recaptcha_response:
            messages.error(
                request,
                "Please complete the reCAPTCHA verification.",
            )

            return render(
                request,
                "control/admin_login.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
                },
            )

        try:
            recaptcha_result = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": recaptcha_response,
                    "remoteip": request.META.get(
                        "REMOTE_ADDR"
                    ),
                },
                timeout=10,
            )

            recaptcha_result.raise_for_status()
            recaptcha_data = recaptcha_result.json()

        except (
            requests.RequestException,
            ValueError,
        ):
            messages.error(
                request,
                "reCAPTCHA verification failed. Please try again.",
            )

            return render(
                request,
                "control/admin_login.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
                },
            )

        if not recaptcha_data.get("success"):
            messages.error(
                request,
                "Please complete the reCAPTCHA verification correctly.",
            )

            return render(
                request,
                "control/admin_login.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
                },
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff and user.is_active:
            cache.delete(rate_limit_key)

            login(
                request,
                user,
            )

            return redirect("admin_dashboard")

        attempts += 1

        cache.set(
            rate_limit_key,
            attempts,
            5 * 7 * 24 * 60 * 60,
        )

        messages.error(
            request,
            "Invalid credentials or not an admin.",
        )

    return render(
        request,
        "control/admin_login.html",
        {
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        },
    )


def admin_logout_view(request):
    logout(request)
    return redirect("admin_login")


@admin_required
def security_controls(request):
    return render(
        request,
        "control/security_controls.html",
    )


@admin_required
def audit_logs(request):
    return render(
        request,
        "control/audit_logs.html",
    )


@admin_required
def email_templates(request):
    return render(
        request,
        "control/email_templates.html",
    )


@admin_required
def platform_management(request):
    return render(
        request,
        "control/platform_management.html",
    )