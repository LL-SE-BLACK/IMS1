# -*- coding: utf-8 -*-
from django.contrib.messages import get_messages

__author__ = 'xyh' #...

from head import *

from models import Student_user
from models import Faculty_user
from models import Admin_user

from profile_forms import StudentInfoForm
from profile_forms import FacultyInfoForm
from profile_forms import AdminInfoForm
from django.http import Http404
from django.contrib import messages

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

IS_STUDENT = -3
IS_Faculty = -2
IS_ADMIN = -1
IS_NOTHING = 0

def getTypeOfUser(user_id):
    user_id_len = user_id.__len__()
    if user_id_len == LEN_OF_STUDENT_ID:
        return IS_STUDENT
    elif user_id_len == LEN_OF_FACULTY_ID:
        return IS_Faculty
    elif user_id_len == LEN_OF_ADMIN_ID:
        return IS_ADMIN
    else: # invalid id length
        return IS_NOTHING

@login_required()
def profile(request):
    user_id = str(request.user)  # user Id
    user_type = getTypeOfUser(user_id)
    # Flags of the previous request of changing infos or passwords
    infoSuccessFlag = False
    infoErrorFlag = False
    infoErrorMessage = []
    passwdErrorFlag = False
    # get messages from the previous request if change info or password
    storage = get_messages(request)
    for message in storage:
        if message.tags == 'profile success':
            infoSuccessFlag = True
        elif message.tags == "profile error":
            infoErrorFlag = True
            infoErrorMessage = message.message
        elif message.tags == "password error":
            passwdErrorFlag = True

    if user_type == IS_STUDENT:
        print "render a student panel"
        stu = Student_user.objects.get(id=user_id)
        if infoSuccessFlag:
            return render_to_response("profile.html", {"isStudent": 1, "userInfo": stu, "infoSuccess": 1})
        elif infoErrorFlag:
            return render_to_response("profile.html", {"isStudent": 1, "userInfo": stu, 'infoErrors':infoErrorMessage})
        elif passwdErrorFlag:
            return render_to_response("profile.html", {"isStudent": 1, "userInfo": stu, 'passwdErrors':1})
        else:
            return render_to_response("profile.html", {"isStudent": 1, "userInfo": stu})
    elif user_type == IS_Faculty:
        try:
            faculty = Faculty_user.objects.get(id=user_id)
        except:
            #return Http404("No such user matched in database")
            print("Internal test data integrity error: no such user matched in database")
            return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))
        if infoSuccessFlag:
            return render_to_response("profile.html", {"isFaculty": 1, "userInfo": faculty, "infoSuccess": 1})
        elif infoErrorFlag:
            return render_to_response("profile.html", {"isFaculty": 1, "userInfo": faculty, 'infoErrors':infoErrorMessage})
        elif passwdErrorFlag:
            return render_to_response("profile.html", {"isFaculty": 1, "userInfo": faculty, 'passwdErrors':1})
        else:
            return render_to_response("profile.html", {"isFaculty": 1, "userInfo": faculty})
    elif user_type == IS_ADMIN:
        admin = Admin_user.objects.get(id=user_id)
        if infoSuccessFlag:
            return render_to_response("profile.html", {"isAdmin": 1, "userInfo": admin, "infoSuccess": 1})
        elif infoErrorFlag:
            return render_to_response("profile.html", {"isAdmin": 1, "userInfo": admin, 'infoErrors':infoErrorMessage})
        elif passwdErrorFlag:
            return render_to_response("profile.html", {"isAdmin": 1, "userInfo": admin, 'passwdErrors':1})
        else:
            return render_to_response("profile.html", {"isAdmin": 1, "userInfo": admin})
    else:
        #wrong id length
        raise Http404("Wrong id length")



#Note: has not finished
@csrf_exempt
@login_required
def changeUserInfo(request):
    if request.method == 'GET':
        print("Change User Info:")
        c = {}
        c.update(csrf(request))
        user = User.objects.get(username=str(request.user))
        if user is None or not user.is_active:
            return HttpResponseRedirect('../home/')
        else: # user exists and valid
            user_type = getTypeOfUser(str(request.user))
            print "user_type:" + str(user_type)
            form = None
            if user_type == IS_STUDENT:
                form = StudentInfoForm(request.GET)
            elif user_type == IS_Faculty:
                form = FacultyInfoForm(request.GET)
            elif user_type == IS_ADMIN:
                form = AdminInfoForm(request.GET)
            else:
                raise  Http404()

            if form.is_valid():
                info = form.cleaned_data
                print request.user
                userid = str(request.user)
                obj = None
                if user_type == IS_STUDENT:
                    obj = Student_user.objects.get(id=userid)
                elif user_type == IS_Faculty:
                    obj = Faculty_user.objects.get(id=userid)
                elif user_type == IS_ADMIN:
                    obj = Admin_user.objects.get(id=userid)

                print("From: " + obj.__unicode__())
                obj.college = info["college"]
                obj.contact = info['contact']
                if info['gender'] == 1:
                    obj.gender = True
                elif info['gender'] == 0:
                    obj.gender = False
                obj.name = info['name']
                if user_type == IS_STUDENT: # Only students have this attributes
                    obj.grade = info['grade']
                    obj.major = info['major']
                obj.save()
                print("To:" + obj.__unicode__())
                messages.success(request, "Profile updates successfully!", extra_tags = "profile")
                return HttpResponseRedirect('../../profile')
                # return render_to_response('profile.html', {'studentInfo':info, 'infoSuccess':1})
            else:
                print("Error: Form invalid!")
                print(str(form.errors))
                # return HttpResponseRedirect('profile.html', {'studentInfo':request.GET, 'infoErrors':form.errors})
                messages.error(request, str(form.errors), extra_tags="profile")
                return HttpResponseRedirect('../../profile')


    else:
        print 'ERROR: not GET'
        raise Http404()

@csrf_exempt  #Note: 如果有人有时间，求帮我看看跨站为啥搞不定。。
@login_required
def changePasswd(request):
    print "Change passwd"
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
            # c.update(errors)
            # stu = Student_user.objects.get(id=str(request.user))
            # c.update({'studentInfo': stu })
            print errors
            messages.error(request, errors, extra_tags="password")
            return HttpResponseRedirect('../../profile')
            # return render_to_response('profile.html', c, context_instance=RequestContext(request))
        else : # success and valid request
            return render_to_response('change_passwd_success.html')
    else:
        print('ERROR: not post')
        raise Http404()








