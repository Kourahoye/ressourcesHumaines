"""
URL configuration for ressourcesHumaines project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/',include('employees.urls')),
    path('accounts/',include('Users.urls')),
    path('departements/',include('departements.urls')),
    path('presence/',include('presences.urls')),
    path('',include('mainpage.urls')),
    path('core/',include("core.urls")),
    path('conges/',include("conges.urls")),
    path('evaluations/',include("evaluations.urls")),
    path('paiments/',include("comptabilite.urls")),
]
