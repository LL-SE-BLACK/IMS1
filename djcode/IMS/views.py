from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
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

def hello(request):
        return render(request,
                      'index.html')

def login(request):
    return render(request, 'login.html')

def loggedin(request):
    c = {}
    c.update(csrf(request))
    #
    userid = request.POST['userid']
    return render_to_response('index.html', c)

def add_user(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('add_user.html', c)

def user_added(request):
    c = {}
    c.update(csrf(request))
    usertype = request.POST['user_type']
    userid = request.POST['user_id']
    userpasswd = '123456' #default
    user = User.objects.create_user(userid, userid+'@zju.edu.cn', userpasswd)
    user.save()
    return render_to_response('add_user.html', c)

def user_auth(request):
    c = {}
    c.update(csrf(request))
    user = authenticate(username = request.POST['user_id'], password = request.POST['user_passwd'])
    if user is not None:
        if user.is_active:
            return HttpResponse(0) #valid, active and authenticated
        else:
            return HttpResponse(2) #user disabled, yet passwd valid
    else:
        return HttpResponse(1) #username or passwd invalid, doesn't match

def login_jump(request):
    c = {}
    c.update(csrf(request))
    print(request.POST)
    userid = request.POST['userid']
    userpasswd = request.POST['userpasswd']
    user = authenticate(username = userid, password = userpasswd)
    login(request, user)
    if (userid.length==10):
        usertype = "Student"
        return render_to_response('panel_for_student.html', c)
    elif (userid.length==6):
        usertype = "Faculty"
        return render_to_response('panel_for_faculty.html', c)
    elif (userid.length==3):
        usertype = "Admin"
        return render_to_response('panel_for_admin.html', c)
    else:
        #error occurs
        logout(request)
