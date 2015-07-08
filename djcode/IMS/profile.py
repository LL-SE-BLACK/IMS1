# -*- coding: utf-8 -*-
from django.contrib.messages import get_messages
from IMS.profile_forms import UserPhotoForm

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
import logging

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

IS_STUDENT = -3
IS_Faculty = -2
IS_ADMIN = -1
IS_NOTHING = 0

logger = logging.getLogger("IMS")

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
    photoErrorFlag = False
    #isStudent, isFaculty, isAdmin, isSuper = 0, 0, 0, 0
    t = get_template('Profile.html')
    c_dict = {}
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
        elif message.tags == "photo error":
            photoErrorFlag = True

    if user_type == IS_STUDENT:
        try:
            stu = Student_user.objects.get(id=user_id)
            c_dict.update({"userInfo": stu, "isStudent": 1})
            if stu.isSpecial:
                if request.user.has_perm('IMS.student_manage') or request.user.has_perm('IMS.faculty_manage') or request.user.has_perm('IMS.admin_manage'):
                    c_dict.update({"manageUser": 1})
                elif request.user.has_perm('IMS.course_manage'):
                    c_dict.update({"manageCourse": 1})
        except:
            #return Http404("No such user matched in database")
            print("Internal test data integrity error: no such user matched in database")
            return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))

    elif user_type == IS_Faculty:
        try:
            faculty = Faculty_user.objects.get(id=user_id)
            c_dict.update({"userInfo": faculty, "isFaculty": 1})
            if faculty.isSpecial:
                if request.user.has_perm('IMS.student_manage') or request.user.has_perm('IMS.faculty_manage') or request.user.has_perm('IMS.admin_manage'):
                    c_dict.update({"manageUser": 1})
                elif request.user.has_perm('IMS.course_manage'):
                    c_dict.update({"manageCourse": 1})
        except:
            #return Http404("No such user matched in database")
            print("Internal test data integrity error: no such user matched in database")
            return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))

    elif user_type == IS_ADMIN:
        try:
            admin = Admin_user.objects.get(id=user_id)
            c_dict.update({"userInfo": admin, "isAdmin": 1})
            if admin.college=='all':
                c_dict.update(({"isSuper": 1}))
        except:
            #return Http404("No such user matched in database")
            print("Internal test data integrity error: no such user matched in database")
            return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))

    else:
        #wrong id length
        print("Wrong in Id length!")
        return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))

    if infoSuccessFlag:
        c_dict.update({'infoSuccess': 1})
    elif infoErrorFlag:
        c_dict.update({'infoErrors': infoErrorMessage})
    elif passwdErrorFlag:
        c_dict.update({'passwdErrors': 1})
    elif photoErrorFlag:
        c_dict.update({'photoErrors': 1})
    else:
        pass
    c = RequestContext(request, c_dict)
    return HttpResponse(t.render(c))


#Note: has not finished
@csrf_exempt
@login_required
def changeUserInfo(request):
    if request.method == 'GET':
        logger.info("Change User Info:")
        c = {}
        c.update(csrf(request))
        user = User.objects.get(username=str(request.user))
        if user is None or not user.is_active:
            return HttpResponseRedirect('../home/')
        else: # user exists and valid
            user_type = getTypeOfUser(str(request.user))
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
                print(request.user)
                userid = str(request.user)
                obj = None
                if user_type == IS_STUDENT:
                    obj = Student_user.objects.get(id=userid)
                elif user_type == IS_Faculty:
                    obj = Faculty_user.objects.get(id=userid)
                elif user_type == IS_ADMIN:
                    obj = Admin_user.objects.get(id=userid)

                logger.info("From: " + obj.__unicode__())
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
                logger.info("To:" + obj.__unicode__())
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
        print('ERROR: not GET')
        raise Http404()

@csrf_exempt  #Note: 如果有人有时间，求帮我看看跨站为啥搞不定。。
@login_required
def changePasswd(request):
    print("Change passwd")
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        errors = {}

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
            messages.error(request, errors, extra_tags="password")
            return HttpResponseRedirect('../../profile')
            # return render_to_response('profile.html', c, context_instance=RequestContext(request))
        else : # success and valid request
            logout(request)
            return render_to_response('change_passwd_success.html')
    else:
        print('ERROR: not post')
        raise Http404()


@csrf_exempt
@login_required
def changePhoto(request):
    # Handle file upload
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = str(request.user)  # user Id
            user_type = getTypeOfUser(user_id)

            newPhoto = form.cleaned_data['photo']
            if user_type == IS_STUDENT:
                try:
                    stu = Student_user.objects.get(id=user_id)
                except:
                    #return Http404("No such user matched in database")
                    print("Internal test data integrity error: no such user matched in database")
                    return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))
                stu.photo = newPhoto
                stu.save()
                return HttpResponseRedirect('../../profile')

            elif user_type == IS_Faculty:
                try:
                    faculty = Faculty_user.objects.get(id=user_id)
                except:
                    #return Http404("No such user matched in database")
                    print("Internal test data integrity error: no such user matched in database")
                    return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))
                faculty.photo = newPhoto
                faculty.save()
                return HttpResponseRedirect('../../profile')

            elif user_type == IS_ADMIN:
                try:
                    admin = Admin_user.objects.get(id=user_id)
                except:
                    #return Http404("No such user matched in database")
                    print("Internal test data integrity error: no such user matched in database")
                    return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))
                admin.photo = newPhoto
                admin.save()
                return HttpResponseRedirect('../../profile')
            else:
                #wrong id length
                print("Wrong in Id length!")
                return HttpResponseRedirect('../../logout/', render(request, 'logout.html'))
        else:
            print("Error: Form invalid!")
            print(str(form.errors))
            messages.error(request, str(form.errors), extra_tags="photo")
            return HttpResponseRedirect('../../profile')

    else:
        print('ERROR: not post')
        raise Http404()








