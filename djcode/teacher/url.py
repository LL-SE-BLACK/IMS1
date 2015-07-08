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
import django.contrib.auth.views as auth_views
from IMS.views import startup
import student.views as student_view
import views as teacher_view
urlpatterns = [
    url(r'^class_list/([0-9a-zA-Z]{0,20})/?$',student_view.ViewClass),
    url(r'^teacher/AddQuestion/$',teacher_view.QuestionAdd),
    url(r'^addform1/$',teacher_view.QuestionAddForm1),
    url(r'^addform2/$',teacher_view.QuestionAddForm2),
    url(r'^teacher/ModifyQuestion/$',teacher_view.QuestionModify),
    url(r'^modify/([0-9a-zA-Z]{20})/$',teacher_view.QuestionM),
    url(r'^teacher/DeleteQuestion/$',teacher_view.QuestionDelete),
    url(r'^delete/([0-9a-zA-Z]{20})/$',teacher_view.QuestionD),
    url(r'^paper/([0-9a-zA-Z]{20})/$',teacher_view.PaperAdjust),
    url(r'^/teacher/paper/([0-9a-zA-Z]{20})/$',teacher_view.PaperAdjust),
    # url(r'^test/$',teacher_view.newf),
    url(r'^teacher/AutoGenerate/$',teacher_view.PaperAutoGenerate),
    url(r'^teacher/PaperManagement/([0-9a-zA-Z]{0,21})/?$',teacher_view.PaperManagement),
    url(r'^Cancel/([0-9a-zA-Z]{20})/$',teacher_view.PaperD),
    url(r'^teacher/ManualGenerate/([0-9a-zA-Z]{0,20})/?$',teacher_view.PaperManualGenerate),
    url(r'^teacher/ManualG/([0-9a-zA-Z]{0,20})/?$',teacher_view.PaperMaG),
    url(r'^teacher/PaperAnalysis/$',teacher_view.PaperAnalysis),
    url(r'^teacher/Analysis/([0-9a-zA-Z]{20})/$',teacher_view.PaperA),
    url(r'^student/ViewPaper/$',student_view.ViewPaper),
    url(r'^student/test/([0-9a-zA-Z]{20})/$',student_view.OnlinePaper),
    url(r'^student/test/score/([0-9a-zA-Z]{20,30})/$',student_view.ReturnScore),
]