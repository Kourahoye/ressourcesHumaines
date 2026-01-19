from django.contrib import admin
from django.urls import include, path

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
sitemaps = {
    "static": StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('employees/',include('employees.urls')),
    path('accounts/',include('Users.urls')),
    path('departements/',include('departements.urls')),
    path('presence/',include('presences.urls')),
    path('',include('mainpage.urls')),
    path('conges/',include("conges.urls")),
    path('evaluations/',include("evaluations.urls")),
    path('paiments/',include("comptabilite.urls")),
    path('recrutements/',include("recrutements.urls")),
   path('attendances/',include("attendances.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('permissions/',include('permissions.urls')),
    path('informations/',include('informations.urls')),
]
