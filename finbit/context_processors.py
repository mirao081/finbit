fromcore.modelsimportSiteFooter


defsite_footer(request):
    return{
"site_footer":SiteFooter.objects.first()
}