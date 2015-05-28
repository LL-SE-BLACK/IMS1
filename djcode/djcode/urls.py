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
from django.contrib import admin
#from IMS import urls as ims_urls
from IMS import views as ims_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^ims/', include(ims_urls)),
    #url(r'^hello/', ims_views.hello),
    url(r'^login/',ims_views.login),
    url(r'^loggedin/',ims_views.loggedin),
    url(r'^add_user/', ims_views.add_user),
    url(r'^user_added/', ims_views.user_added),
    url(r'^user_auth/', ims_views.user_auth),
    url(r'^home/', ims_views.login_jump),
]
