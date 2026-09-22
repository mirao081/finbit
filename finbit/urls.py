
"""
URL configuration for finbit project.
"""

fromdjango.contribimportadmin
fromdjango.urlsimportinclude,path
fromaccounts.viewsimportsignup
fromdjango.confimportsettings
fromdjango.conf.urls.staticimportstatic


urlpatterns=[
path("admin/",admin.site.urls),
path("",include("core.urls")),
path("accounts/",include("accounts.urls")),
path("control/",include("control.urls")),
path("signup/",signup,name="signup"),


path("i18n/",include("django.conf.urls.i18n")),
]


ifsettings.DEBUG:
    urlpatterns+=static(
settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT,
)

