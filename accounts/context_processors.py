from core.models import SiteSettings, MenuItem
from .models import DashboardMenu


def sidebar_context(request):
    return {
        "site_settings": SiteSettings.objects.first(),
        "menu_items": MenuItem.objects.filter(is_active=True),
        "menus": DashboardMenu.objects.all(),
    }


from .models import UserProfile


def user_dashboard_context(request):

    if not request.user.is_authenticated:
        return {}

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return {
        "user_profile": profile,
    }