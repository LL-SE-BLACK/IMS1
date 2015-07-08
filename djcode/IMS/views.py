# -*- coding: utf-8 -*-

from IMS.head import *
from IMS.models import Student_user, Faculty_user, Admin_user
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
            super(LoginForm, self).errors['username'] = ErrorList(error_msg)
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
    #print request.user
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
    isStudent, isFaculty, isAdmin, isSuper = 0, 0, 0, 0

    if user_name_len == LEN_OF_STUDENT_ID:
        usrInfo = Student_user.objects.get(id=user_name)
        isStudent = 1
        #return render_to_response('home_panel.html', {"isStudent": 1, "usrInfo": usrInfo})
    elif user_name_len == LEN_OF_FACULTY_ID:
        usrInfo = Faculty_user.objects.get(id=user_name)
        isFaculty = 1
        #return render_to_response('home_panel.html', {"isFaculty": 1, "usrInfo": usrInfo})
    elif user_name_len == LEN_OF_ADMIN_ID:
        usrInfo = Admin_user.objects.get(id=user_name)
        isAdmin = 1
        if usrInfo.college == "all":
            isSuper = 1
    else:
        # wrong id length
        raise Http404()

    t = get_template('home_panel.html')
    c_dict = {"usrInfo": usrInfo, "isStudent": isStudent, "isFaculty": isFaculty,
              "isAdmin": isAdmin, "isSuper": isSuper}
    if not isAdmin:
        if usrInfo.isSpecial:
            c_dict.update({"isSpecial": 1})
            if request.user.has_perm('IMS.student_manage'):
                c_dict.update({"manageStudent": 1})
            elif request.user.has_perm('IMS.faculty_manage'):
                c_dict.update({"manageFaculty": 1})
            elif request.user.has_perm('IMS.admin_manage'):
                c_dict.update({"manageAdmin": 1})
            elif request.user.has_perm('IMS.course_manage'):
                c_dict.update({"manageCourse": 1})
    c = RequestContext(request, c_dict)
    return HttpResponse(t.render(c))