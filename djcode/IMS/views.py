# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from django.http import HttpResponseRedirect
from django.core.files import File
import re
import os
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from models import Student_user

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

def startup(request):
    if not request.user.is_authenticated():
        print "not authenticated"
        # return render(request, 'add_user.html')
        return render(request, 'login.html')
    else:
        print 'authenticated'
        return HttpResponseRedirect('../home/')

def loggingout(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def add_user(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('add_user.html', c)

@login_required
def user_added(request):
    c = {}
    c.update(csrf(request))
    print(request.POST)
    usertype = request.POST['user_type']
    userid = request.POST['user_id']
    userpasswd = '123456' #default
    user = User.objects.create_user(userid, userid+'@zju.edu.cn', userpasswd)
    if usertype == 'Admin':
        user.user_permissions.add()
    elif usertype == 'Student':
        newStudent = Student_user(id=userid)
        newStudent.save()
        print 'newStudent:',newStudent
    elif usertype == 'Faculty':
        pass
        #TODO add a faculty to database
    user.save()
    return render_to_response('add_user.html', c)

def user_auth(request):
    c = {}
    c.update(csrf(request))

    t = get_template('login.html')
    user = authenticate(username = request.POST['userid'], password = request.POST['userpasswd'])
    if user is not None:
        if user.is_active: #valid, active and authenticated
            login(request, user)
            return HttpResponseRedirect('../home/')
        else:
            return HttpResponseRedirect('../', t.render(Context({'forbidden': 1}))) #user disabled, yet passwd valid
    else:
        print('nomatch')
        return HttpResponseRedirect('../', t.render(Context({'no_match': 1}))) #username or passwd invalid, doesn't match

@login_required
def home(request):
    user_name = str(request.user)  # user Id
    user_name_len = user_name.__len__()
    if user_name_len == LEN_OF_STUDENT_ID:
        stu = Student_user.objects.get(id=user_name)
        return render_to_response('panel_for_student.html',{'studentInfo':stu})
    elif user_name_len == LEN_OF_FACULTY_ID:
        t = get_template('panel_for_faculty.html')
        return HttpResponse(t.render())
    elif user_name_len == LEN_OF_ADMIN_ID:
        t = get_template('panel_for_admin.html')
        return HttpResponse(t.render())

#Note: has not finished
@csrf_exempt
@login_required
def changeStudentInfo(request):
    print "change student info"
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        #TODO
    else:
        print 'ERROR: not post'
    return render_to_response('panel_for_student.html', {'studentInfo':request.POST})

@csrf_exempt  #Note: 如果有人有时间，求帮我看看跨站为啥搞不定。。
@login_required
def changePasswd(request):
    print "change passwd"
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        errors = {}

        print(request.POST)
        passwd1 = request.POST.get("passwd1","")
        passwd2 = request.POST.get("passwd2","")
        if not passwd1 == passwd2:
            errors.update({'passwdErrors':1})
        else:
            if len(passwd1) > 20 or len(passwd1) < 5:
                errors.update({'passwdErrors':2})
            else:
                user = User.objects.get(username=str(request.user))
                print(user)
                user.set_password(passwd1)
                user.save()
        if errors.get('passwdErrors') == 1 or errors.get('passwdErrors') == 2:
            c.update(errors)
            stu = Student_user.objects.get(id=str(request.user))
            c.update({'studentInfo': stu })
            return render_to_response('panel_for_student.html', c, context_instance=RequestContext(request))
        else : # success and valid request
            return render_to_response('change_passwd_success.html', {'studentInfo':c}, context_instance=RequestContext(request))
    else:
        print('ERROR: not post')




