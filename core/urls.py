fromdjango.urlsimportpath
from.importviews

urlpatterns=[
path('',views.home,name='home'),
path('about/',views.about,name='about'),
path('plan/',views.plan,name='plan'),
path('blog/',views.blog,name='blog'),
path('contact/',views.contact,name='contact'),
path('plans/',views.all_plans,name='all_plans'),
path("crypto-stats/",views.crypto_stats,name="crypto_stats"),
path("news/",views.news_list,name="news_list"),
path("news/<int:pk>/",views.news_detail,name="news_detail"),
path("privacy-policy/",views.privacy_policy,name="privacy_policy"),
path("terms-conditions/",views.terms_conditions,name="terms_conditions"),

]
fromdjango.confimportsettings
fromdjango.conf.urls.staticimportstatic

ifsettings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)