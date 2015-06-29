# -*- coding: utf-8 -*-

from head import *
from models import Student_user
from profile_forms import StudentInfoForm
from django.http import Http404
from django import forms
from django.forms.util import ErrorList

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    passwd = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        _username = cleaned_data.get('username', '')
        _passwd = cleaned_data.get('passwd', '')
        if not User.objects.filter(username=_username):
            error_msg = ["用户不存在！"]
            super(LoginForm, self).errors['passwd'] = ErrorList(error_msg)
        else:
            user = authenticate(username=_username, password=_passwd)
            if user is None:
                error_msg = ["密码错误!"]
                super(LoginForm, self).errors['passwd'] = ErrorList(error_msg)
                #raise forms.ValidationError('密码错误')
        return cleaned_data

def startup(request):
    return HttpResponseRedirect('ims/login/')

def loggingin(request):
    if not request.user.is_authenticated():
        form = LoginForm()
        t = get_template('login.html')
        c = RequestContext(request, {'form': form})
        return HttpResponse(t.render(c))
    else:
        return HttpResponseRedirect('../home/')

@login_required
def loggingout(request):
    logout(request)
    #return render(request, 'logout.html')
    return HttpResponseRedirect('../login/')

@login_required
def add_user(request):
    print("add_user")
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
    print("haha")
    user = User.objects.create_user(userid, userid+'@zju.edu.cn', userpasswd)
    if usertype == 'Admin':
        user.user_permissions.add()
    elif usertype == 'Student':
        if len(userid) != 10:
            c.update({'idLenInvalid':1})
        else:
            newStudent = Student_user(id=userid)
            newStudent.save()
            #print 'newStudent:',newStudent
    elif usertype == 'Faculty':
        pass
        #TODO add a faculty to database
    user.save()
    return render_to_response('add_user.html', c)

@csrf_exempt
def user_auth(request):
    #c = {}
    #c.update(csrf(request))
    form = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()

    if form.is_valid():
        _username = form.cleaned_data['username']
        _passwd = form.cleaned_data['passwd']
        user = authenticate(username = _username, password = _passwd)
        if user is not None:
            if user.is_active: #valid, active and authenticated
                login(request, user)
                return HttpResponseRedirect('../home/')  #TODO: csrf

    # else, back to login page
    t = get_template('login.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))

@csrf_exempt
@login_required
def home(request):
    user_name = str(request.user)  # user Id
    user_name_len = user_name.__len__()
    if user_name_len == LEN_OF_STUDENT_ID:
        # stu = Student_user.objects.get(id=user_name)
        return render_to_response('home_panel.html',{"isStudent": 1, "id" : user_name})
    elif user_name_len == LEN_OF_FACULTY_ID:
        return render_to_response('home_panel.html',{"isFaculty": 1, "id" : user_name})
    elif user_name_len == LEN_OF_ADMIN_ID:
        return render_to_response('home_panel.html',{"isAdmin": 1, "id" : user_name})
    else:
        # wrong id length
        raise Http404()