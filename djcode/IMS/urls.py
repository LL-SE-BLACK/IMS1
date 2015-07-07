__author__ = 'Adward'

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
from django.conf import settings
from django.conf.urls.static import static
from IMS import views, profile, course_views, user_views, log_views, forget_pwd

urlpatterns = [
    url(r'^login/$', views.loggingin), #by adward
    #url(r'^hello/', views.startup),
    url(r'^add_user/', views.add_user), #by adward
    url(r'^user_added/', views.user_added), #by adward
    url(r'^user_auth/', views.user_auth), #by adward
    url(r'^home/$', views.home), #by adward
    url(r'^logout/$', views.loggingout), #by adward
    url(r'^home/profile/$', profile.profile), #by adward
    url(r'^home/profile/changeUserInfo/$', profile.changeUserInfo), #by xyh
    url(r'^home/profile/changePasswd/$', profile.changePasswd), #by xyh
    url(r'^home/profile/changePhoto/$', profile.changePhoto), #by xyh
    url(r'^log/$', log_views.all_log), # by xyh
    url(r'^log/deleteLog/$', log_views.delete_all_log), # by xyh
    url(r'^course/$', course_views.courseMain), #by saltless
    url(r'^course/add/$', course_views.courseAdd), #by saltless
    url(r'^course/delete/$', course_views.courseDelete), #by saltless
    url(r'^course/modify/$', course_views.courseModify), #by saltless
    url(r'^user/$', user_views.userMain), #by Henry
    url(r'^user/add_faculty/$', user_views.facultyAdd), #by Henry
    url(r'^user/delete_faculty/$', user_views.facultyDelete), #by Henry
    url(r'^user/modify_faculty/$', user_views.facultyModify), #by Henry
    url(r'^user/add_student/$', user_views.studentAdd), #by Henry
    url(r'^user/delete_student/$', user_views.studentDelete), #by Henry
    url(r'^user/modify_student/$', user_views.studentModify), #by Henry
    url(r'^user/add_admin/$', user_views.adminAdd), #by Henry
    url(r'^user/delete_admin/$', user_views.adminDelete), #by Henry
    url(r'^user/modify_admin/$', user_views.adminModify), #by Henry
    url(r'^forget_pwd/$', forget_pwd.forget_pwd), #by adward
    url(r'^reset_pwd_mail/$', forget_pwd.reset_pwd_mail), #by adward
    url(r'^reset_pwd/(?P<key>[0-9a-zA-Z]{20})/$', forget_pwd.reset_pwd), #by adward
]

## For upload user photos
urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
