# -*- coding: utf-8 -*-
__author__ = 'xyh' #...

from head import *

from models import Student_user
from student_forms import StudentInfoForm

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

#Note: has not finished
@csrf_exempt
@login_required
def changeStudentInfo(request):
    if request.method == 'GET':
        print("Change Student Info:")
        c = {}
        c.update(csrf(request))
        user = User.objects.get(username=str(request.user))
        if user is None or not user.is_active:
            return HttpResponseRedirect('../home/')
        else: # user exists and valid
            form = StudentInfoForm(request.GET)
            if form.is_valid():
                info = form.cleaned_data
                print request.user
                userid = str(request.user)
                stu = Student_user.objects.get(id=userid)
                print("From: " + stu.__unicode__())
                stu.college = info["college"]
                stu.contact = info['contact']
                if info['gender'] == 1:
                    stu.gender = True
                elif info['gender'] == 0:
                    stu.gender = False
                stu.grade = info['grade']
                stu.major = info['major']
                stu.name = info['name']
                stu.save()
                print("To:" + stu.__unicode__())
                return render_to_response('change_student_info.html', {'studentInfo':info, 'infoSuccess':1})
            else:
                print("Error: Form invalid!")
                print(form.errors)
                return render_to_response('change_student_info.html', {'studentInfo':request.GET, 'infoErrors':form.errors})

    else:
        print 'ERROR: not GET'


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
            return render_to_response('change_student_info.html', c, context_instance=RequestContext(request))
        else : # success and valid request
            return render_to_response('change_passwd_success.html', {'studentInfo':c}, context_instance=RequestContext(request))
    else:
        print('ERROR: not post')







