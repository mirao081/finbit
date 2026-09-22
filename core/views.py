from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    SiteSettings,
    MenuItem,
    InvestmentPlan,
    CryptoStat,
    FeatureCard,
    FeatureSection,
    ProfitCalculatorSection,
    ThreeStepSection,
    Testimonial,
    TeamMember,
    Transaction,
    Investor,
    GetStartedSection,
    PaymentSection,
    PaymentMethod,
    NewsSection,
    NewsItem,
    SiteFooter,
    NewsCategory,
    SiteMap,
    SupportInfo,
    ComplianceNotice,
    SocialLink,
    NewsletterSignup,
)
from .services import get_crypto_data
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import NewsCommentForm, ContactMessageForm, NewsletterSignupForm
from accounts.models import UserProfile
from django.db.models import Sum
from urllib.parse import urlencode


def home(request):
    referral_token = request.GET.get("ref")

    if referral_token:
        return redirect(
            f"/signup/?{urlencode({'ref': referral_token})}"
        )

    site_settings = SiteSettings.objects.first()

    menu_items = MenuItem.objects.filter(
        is_active=True
    )

    plans = InvestmentPlan.objects.all()

    crypto = get_crypto_data()

    section = FeatureSection.objects.first()

    feature_cards = FeatureCard.objects.filter(
        section=section,
        is_active=True
    )[:10]

    profit_section = ProfitCalculatorSection.objects.first()

    three_step_section = (
        ThreeStepSection.objects
        .prefetch_related("steps")
        .first()
    )

    testimonials = Testimonial.objects.all()

    team_members = TeamMember.objects.all()

    activity_type = request.GET.get(
        "activity_type",
        "deposit"
    )

    transactions = (
        Transaction.objects
        .filter(
            transaction_type=activity_type
        )
        .select_related(
            "investor",
            "investor__user",
            "investor__user__userprofile",
            "wallet",
        )
        .order_by("-date")
    )

    paginator_tx = Paginator(
        transactions,
        5
    )

    page_number_tx = request.GET.get(
        "tx_page"
    )

    page_obj_tx = paginator_tx.get_page(
        page_number_tx
    )

    investors = (
        Investor.objects
        .select_related("user")
        .annotate(
            current_investment=Sum(
                "user__investments__amount_usd"
            )
        )
        .order_by(
            "-current_investment"
        )
    )

    paginator_inv = Paginator(
        investors,
        8
    )

    page_number_inv = request.GET.get(
        "inv_page"
    )

    page_obj_inv = paginator_inv.get_page(
        page_number_inv
    )

    get_started = GetStartedSection.objects.first()

    payment_section = PaymentSection.objects.first()

    payment_methods = PaymentMethod.objects.filter(
        section=payment_section,
        is_active=True
    )

    news_section = NewsSection.objects.first()

    news_items = (
        NewsItem.objects
        .filter(
            is_active=True
        )
        .order_by("-date")
    )

    paginator_news = Paginator(
        news_items,
        3
    )

    page_number_news = request.GET.get(
        "news_page"
    )

    news_page_obj = paginator_news.get_page(
        page_number_news
    )

    footer = SiteFooter.objects.first()

    context = {
        "site_settings": site_settings,
        "menu_items": menu_items,
        "plans": plans,
        "crypto": crypto,
        "section": section,
        "feature_cards": feature_cards,
        "profit_section": profit_section,
        "three_step_section": three_step_section,
        "testimonials": testimonials,
        "team_members": team_members,
        "page_obj_tx": page_obj_tx,
        "activity_type": activity_type,
        "page_obj_inv": page_obj_inv,
        "get_started": get_started,
        "payment_section": payment_section,
        "payment_methods": payment_methods,
        "news_section": news_section,
        "news_page_obj": news_page_obj,
        "footer": footer,
    }

    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":
        return render(
            request,
            "core/_news_content.html",
            context
        )

    return render(
        request,
        "core/home.html",
        context
    )


def about(request):
    three_step_section = (
        ThreeStepSection.objects
        .prefetch_related("steps")
        .first()
    )

    team_members = TeamMember.objects.all()
    footer = SiteFooter.objects.first()
    testimonials = Testimonial.objects.all()

    return render(
        request,
        "core/about.html",
        {
            "site_settings": SiteSettings.objects.first(),
            "menu_items": MenuItem.objects.filter(
                is_active=True
            ),
            "three_step_section": three_step_section,
            "team_members": team_members,
            "footer": footer,
            "testimonials": testimonials,
        },
    )


def plan(request):
    site_settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.filter(
        is_active=True
    )
    plans = InvestmentPlan.objects.all()
    footer = SiteFooter.objects.first()

    return render(
        request,
        "core/plan.html",
        {
            "site_settings": site_settings,
            "menu_items": menu_items,
            "plans": plans,
            "footer": footer,
        },
    )


def blog(request):
    site_settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.filter(
        is_active=True
    )
    news_section = NewsSection.objects.first()

    news_list = (
        NewsItem.objects
        .all()
        .order_by("-date")
    )

    paginator = Paginator(
        news_list,
        3
    )

    page_number = request.GET.get(
        "news_page"
    )

    news_page_obj = paginator.get_page(
        page_number
    )

    footer = SiteFooter.objects.first()

    return render(
        request,
        "core/blog.html",
        {
            "site_settings": site_settings,
            "menu_items": menu_items,
            "news_section": news_section,
            "news_page_obj": news_page_obj,
            "footer": footer,
        },
    )


def contact(request):
    site_map = SiteMap.objects.first()
    support_cards = SupportInfo.objects.all()
    compliance_notices = ComplianceNotice.objects.all()
    social_links = SocialLink.objects.all()

    form = ContactMessageForm()
    newsletter_form = NewsletterSignupForm()

    if request.method == "POST":

        if "newsletter" in request.POST:
            email = request.POST.get(
                "email",
                ""
            ).strip()

            if NewsletterSignup.objects.filter(
                email=email
            ).exists():

                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest":
                    return JsonResponse({
                        "status": "exists",
                        "message": "You're already subscribed!"
                    })

                return redirect("contact")

            newsletter_form = NewsletterSignupForm(
                request.POST
            )

            if newsletter_form.is_valid():
                newsletter_form.save()

                if request.headers.get(
                    "X-Requested-With"
                ) == "XMLHttpRequest":
                    return JsonResponse({
                        "status": "ok"
                    })

                return redirect("contact")

            if request.headers.get(
                "X-Requested-With"
            ) == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "error",
                        "errors": newsletter_form.errors,
                    },
                    status=400,
                )

        else:
            form = ContactMessageForm(
                request.POST
            )

            if form.is_valid():
                form.save()
                return redirect("contact")

    return render(
        request,
        "core/contact.html",
        {
            "form": form,
            "newsletter_form": newsletter_form,
            "site_settings": SiteSettings.objects.first(),
            "menu_items": MenuItem.objects.filter(
                is_active=True
            ),
            "footer": SiteFooter.objects.first(),
            "site_map": site_map,
            "support_cards": support_cards,
            "compliance_notices": compliance_notices,
            "social_links": social_links,
        },
    )


def all_plans(request):
    site_settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.filter(
        is_active=True
    )
    plans = InvestmentPlan.objects.all()
    footer = SiteFooter.objects.first()

    return render(
        request,
        "core/all_plans.html",
        {
            "site_settings": site_settings,
            "menu_items": menu_items,
            "plans": plans,
            "footer": footer,
        },
    )


def crypto_stats(request):
    data = get_crypto_data()
    return JsonResponse(data)


def news_list(request):
    section = NewsSection.objects.first()

    news_items = (
        NewsItem.objects
        .filter(is_active=True)
        .order_by("-date")
    )

    paginator = Paginator(
        news_items,
        6
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "core/news_list.html",
        {
            "section": section,
            "page_obj": page_obj,
        },
    )


def news_detail(request, pk):
    site_settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.filter(
        is_active=True
    )
    footer = SiteFooter.objects.first()

    item = get_object_or_404(
        NewsItem,
        pk=pk
    )

    if request.method == "POST":
        form = NewsCommentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            comment = form.save(
                commit=False
            )

            comment.news = item
            comment.save()

            return redirect(
                "news_detail",
                pk=pk
            )

    else:
        form = NewsCommentForm()

    categories = NewsCategory.objects.all()

    archives = NewsItem.objects.dates(
        "date",
        "month",
        order="DESC"
    )

    popular_posts = (
        NewsItem.objects
        .filter(is_active=True)
        .exclude(pk=item.pk)
        .order_by("-date")[:4]
    )

    context = {
        "site_settings": site_settings,
        "menu_items": menu_items,
        "footer": footer,
        "item": item,
        "form": form,
        "categories": categories,
        "archives": archives,
        "popular_posts": popular_posts,
    }

    if request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest":

        return render(
            request,
            "core/_news_details_partial.html",
            context
        )

    return render(
        request,
        "core/news_detail.html",
        context
    )


def privacy_policy(request):
    return render(
        request,
        "core/privacy_policy.html",
        {
            "site_settings": SiteSettings.objects.first(),
            "menu_items": MenuItem.objects.all(),
            "footer": SiteFooter.objects.first(),
        },
    )


def terms_conditions(request):
    return render(
        request,
        "core/terms_conditions.html",
        {
            "site_settings": SiteSettings.objects.first(),
            "footer": SiteFooter.objects.first(),
            "menu_items": MenuItem.objects.all(),
        },
    )