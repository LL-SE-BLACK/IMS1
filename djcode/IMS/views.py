# -*- coding: utf-8 -*-

from head import *
from models import Student_user
from student_forms import StudentInfoForm

LEN_OF_STUDENT_ID = 10
LEN_OF_FACULTY_ID = 6
LEN_OF_ADMIN_ID = 3

def startup(request):
    return HttpResponseRedirect('ims/')

def loggingin(request):
    if not request.user.is_authenticated():
        print "not authenticated"
        # return render(request, 'add_user.html')
        return render(request, 'login.html')
    else:
        print 'authenticated'
        return HttpResponseRedirect('home/')

@login_required
def loggingout(request):
    logout(request)
    return render(request, 'logout.html')

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

@csrf_exempt
@login_required
def home(request):
    user_name = str(request.user)  # user Id
    user_name_len = user_name.__len__()
    if user_name_len == LEN_OF_STUDENT_ID:
        stu = Student_user.objects.get(id=user_name)
        return render_to_response('change_student_info.html',{'studentInfo':stu})
    elif user_name_len == LEN_OF_FACULTY_ID:
        t = get_template('panel_for_faculty.html')
        return HttpResponse(t.render())
    elif user_name_len == LEN_OF_ADMIN_ID:
        t = get_template('panel_for_admin.html')
        return HttpResponse(t.render())