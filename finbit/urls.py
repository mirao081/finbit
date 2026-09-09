
"""
URL configuration for finbit project.
"""

from django.contrib import admin
from django.urls import include, path
from accounts.views import signup
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("control/", include("control.urls")),
    path("signup/", signup, name="signup"),

    # Django internationalization / language switching
    path("i18n/", include("django.conf.urls.i18n")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

