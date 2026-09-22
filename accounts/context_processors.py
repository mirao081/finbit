fromcore.modelsimportSiteSettings,MenuItem
from.modelsimportDashboardMenu

defsidebar_context(request):
    return{
"site_settings":SiteSettings.objects.first(),
"menu_items":MenuItem.objects.filter(is_active=True),
"menus":DashboardMenu.objects.all(),
}


from.modelsimportUserProfile


defuser_dashboard_context(request):

    ifnotrequest.user.is_authenticated:
        return{}

profile,created=UserProfile.objects.get_or_create(
user=request.user
)

return{
"user_profile":profile,
}