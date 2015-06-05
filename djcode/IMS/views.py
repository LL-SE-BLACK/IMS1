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

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

def startup(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
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
    user = User.objects.create_user(userid[0], userid[0]+'@zju.edu.cn', userpasswd)
    if usertype=='Admin':
        user.user_permissions.add()
    elif usertype=='Student':
        #pass
        #TODO add a student to database
    elif usertype=='Faculty':
        #pass
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
    user_name = str(request.user)
    user_name_len = user_name.__len__()
    if user_name_len == LEN_OF_STUDENT_ID:
        t = get_template('panel_for_student.html')
        return HttpResponse(t.render()) #TODO pass user info to homepage panel
    elif user_name_len == LEN_OF_FACULTY_ID:
        t = get_template('panel_for_faculty.html')
        return HttpResponse(t.render())
    elif user_name_len == LEN_OF_ADMIN_ID:
        t = get_template('panel_for_admin.html')
        return HttpResponse(t.render())