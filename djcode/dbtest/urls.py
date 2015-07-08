from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login', views.score_login),
    url(r'^logout', views.score_logout),
    url(r'^query', views.score_query),
    url(r'^program_query', views.program_query),
    url(r'^commit', views.score_commit),
    url(r'^modification', views.score_modification),
    url(r'^B_student_query', views.b_student_query),
    url(r'^B_teacher_query', views.b_teacher_query),
    url(r'^B_teacher_temp_query', views.b_teacher_temp_query),
    url(r'^B_temp_table_query/(?P<c_id>\d+)', views.b_temp_table_query),
    url(r'^B_temp_class_score_query/(?P<c_id>\d+)', views.b_temp_class_score_query),
    url(r'^B_final_class_score_query/(?P<c_id>\d+)', views.b_final_class_score_query),
    url(r'^B_score_modification/(?P<c_id>\d+)/(?P<s_id>\d+)', views.B_score_modification),
    url(r'^B_query_modify_info', views.b_query_modify_info),
    url(r'^B_sanction_result/(?P<msg_id>\d+)/(?P<status>[01])', views.b_sanction),
    url(r'^B_upload_xlsx/(?P<c_id>\d+)', views.upload_xlsx),
    url(r'^B_download_xlsx/(?P<c_id>\d+)', views.download_xlsx),
    url(r'^B_finalCommit/(?P<c_id>\d+)', views.b_final_commit),
    url(r'^B_online_save/(?P<s_id>\d+)/(?P<c_id>\d+)', views.b_online_save),
    url(r'^B_scheme_info', views.get_scheme_info),
]
