from core.models import SiteFooter


def site_footer(request):
    return {
        "site_footer": SiteFooter.objects.first()
    }