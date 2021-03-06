"""vulner_db_serv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.static import serve

from .views import test_view
from .views import common_views

urlpatterns = [
    # url(r'^static/(?P<path>.)$', serve, {"document_root": settings.STATIC_ROOT})
    path('admin/', admin.site.urls),
    path('test/', test_view.index, name='index'),
    path('test/edb', test_view.fetch_exploit_db, name='testedb'),
    path('cnvd/', include('cnvd.urls')),

    path('account-manage/', include('account_manage.urls')),
    path('edb/', include('edb.urls')),
    path('set_user/', common_views.set_user, name='set_user'),
    path('get_user/', common_views.get_user, name='get_user'),
]
