"""djcode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.views as auth_views
from IMS.views import startup
from djcode import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #by SMS

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ims/', include('IMS.urls')),
    url(r'^SM/', include('dbtest.urls')), #by SMS
    url(r'^$', startup),
]

urlpatterns += staticfiles_urlpatterns() #by SMS

