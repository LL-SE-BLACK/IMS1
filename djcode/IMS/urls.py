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
from IMS import views, change_student_personal_info, course_views

urlpatterns = [
    url(r'^$', views.loggingin),
    #url(r'^hello/', views.startup),
    url(r'^add_user/', views.add_user),
    url(r'^user_added/', views.user_added),
    url(r'^user_auth/', views.user_auth),
    url(r'^home/', views.home),
    url(r'^logout/', views.loggingout),
    url(r'^changeStudentInfo/', change_student_personal_info.changeStudentInfo), #by xyh
    url(r'^changePasswd/', change_student_personal_info.changePasswd), #by xyh
    url(r'^course/$', course_views.courseMain), #by saltless
    url(r'^course/add/$', course_views.courseAdd), #by saltless
    url(r'^course/delete/$', course_views.courseDelete), #by saltless
    url(r'^course/modify/$', course_views.courseModify), #by saltless
]