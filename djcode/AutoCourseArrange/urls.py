"""mysite URL Configuration

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
import AutoCourseArrange.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
	#url(r'^time/plus/(\d{1,2})/$', hours_ahead),
	url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
	url(r'^cr/(add|del|mod|)?$', views.TeachingResourse),
	url(r'^acs/(automatic)?$', views.CourseArrange),
	url(r'^mca/(add_cl|del_cl|)?$', views.CourseApply),
	url(r'^(admin|teacher)?$', views.Index),
	url(r'^tcs/', views.CourseSearch),
	url(r'^ci/', views.ClassroomInquiry),
	url(r'^course/(add_cz|del_cz|add_cl|del_cl|)?$', views.CourseOperation),
	url(r'^logout/', views.Logout),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 