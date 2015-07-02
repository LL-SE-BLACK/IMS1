__author__ = 'John'

from head import *
import re
import os

from models import Class_info, Course_info, Faculty_user, Admin_user, Student_user
from user_forms import StudentForm, FacultyForm, StudentFormModify, FacultyFormModify, AdminForm, AdminFormModify

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group,Permission

LEN_OF_FACULTY_TABLE = 8
LEN_OF_STUDENT_TABLE = 9
LEN_OF_ADMIN_TABLE = 5

@login_required
def userMain(request):
    canManageStudent = True
    canManageFaculty = True
    canManageAdmin = False
    admin = Admin_user.objects.filter(id = request.user.username)
    if admin:
        if admin[0].college == 'all':
            canManageAdmin = True
        return render(request, 'UserMain.html', locals())
    else:
        userInfo = Faculty_user.objects.filter(id = request.user.username)
        if userInfo:
            if userInfo[0].isSpecial:
                if not request.user.has_perm("IMS.student_manage"):
                    canManageStudent = False
                if not request.user.has_perm("IMS.faculty_manage"):
                    canManageFaculty = False
                return render(request, 'UserMain.html', locals())
            else:
                return render(request, 'AccessFault.html')
        else:
            userInfo = Student_user.objects.filter(id = request.user.username)
            if userInfo[0].isSpecial:
                if not request.user.has_perm("IMS.student_manage"):
                    canManageStudent = False
                if not request.user.has_perm("IMS.faculty_manage"):
                    canManageFaculty = False
                return render(request, 'UserMain.html', locals())
            else:
                return render(request, 'AccessFault.html')

def isDigit(a):
    for x in a:
        if not ((x >= '0' and x <= '9') or x == '.'):
            return False
    pos = a.find('.')
    if pos < 0:
        return 'INT'
    else:
        if a[pos + 1: ].find('.') < 0:
            return 'FLOAT'
        else:
            return False

def importFacultyCheck(term):
    if Faculty_user.objects.filter(id = term[0]): #test duplicate add
        return 'ALREADY EXIST'
    if len(term[0]) > 6:
        return 'ID: TOO LONG'
    if len(term[1]) > 11:
        return 'CONTACT: TOO LONG'
    if len(term[2]) > 20:
        return 'NAME: TOO LONG'
    if len(term[4]) > 50:
        return 'COLLEGE: TOO LONG'
    if len(term[5]) > 50:
        return 'MAJOR: TOO LONG'
    if len(term[6]) > 20:
        return 'DEGREE: TOO LONG'
    if len(term[7]) > 20:
        return 'TITLE: TOO LONG'
    return 'YEAH'

def importStudentCheck(term):
    if Student_user.objects.filter(id = term[0]): #test duplicate add
        return 'ALREADY EXIST'
    if len(term[0]) > 10:
        return 'ID: TOO LONG'
    if len(term[1]) > 11:
        return 'CONTACT: TOO LONG'
    if len(term[2]) > 20:
        return 'NAME: TOO LONG'
    if len(term[4]) > 50:
        return 'COLLEGE: TOO LONG'
    if len(term[5]) > 50:
        return 'MAJOR: TOO LONG' 
    return 'YEAH'

def importAdminCheck(term):
    if Admin_user.objects.filter(id = term[0]): #test duplicate add
        return 'ALREADY EXIST'
    if len(term[0]) > 6:
        return 'ID: TOO LONG'
    if len(term[1]) > 11:
        return 'CONTACT: TOO LONG'
    if len(term[2]) > 20:
        return 'NAME: TOO LONG'
    if len(term[4]) > 50:
        return 'COLLEGE: TOO LONG'
    if len(term[5]) > 50:
        return 'MAJOR: TOO LONG'
    return 'YEAH'

def getSearchResult(searchType, searchTerm, userCollege, userType):
    if userType == 'ADMIN':
        if searchType == "id":
            Temp = Admin_user.objects.filter(id = searchTerm)
        if searchType == "name":
            Temp = Admin_user.objects.filter(name__icontains = searchTerm)
    elif userType == 'FACULTY':
        if searchType == "id":
            Temp = Faculty_user.objects.filter(id = searchTerm)
        if searchType == "name":
            Temp = Faculty_user.objects.filter(name__icontains = searchTerm)
    elif userType == 'STUDENT':
        if searchType == "id":
            Temp = Student_user.objects.filter(id = searchTerm)
        if searchType == "name":
            Temp = Student_user.objects.filter(name__icontains = searchTerm)

    if userCollege != 'all':
        Temp = Temp.filter(college = userCollege)
    results = []
    for result in Temp:
        results.append(result)
    return results

@login_required
def facultyAdd(request):
    errors = []
    errorImport = []
    existed = []
    addIsDone = False
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    isSuper = False
    if userCollege == 'all':
        isSuper = True

    if request.method == 'POST':
        if request.POST.get('multiAddCancel') or request.POST.get('first'): #click cancle button or first access
            form = FacultyForm(initial={'college' : userCollege})
        elif 'file' in request.POST and len(request.POST.get('file')) > 0:  # click confirm button
            fileTerms = re.split(',', request.POST.get('file'))
            for x in range(0, len(fileTerms) / LEN_OF_FACULTY_TABLE):
                dbQuery = Faculty_user(
                    id = fileTerms[0 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    contact = fileTerms[1 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    name = fileTerms[2 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    gender = fileTerms[3 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    college = fileTerms[4 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    major = fileTerms[5 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    degree = fileTerms[6 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    title = fileTerms[7 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                )
                state = importFacultyCheck(fileTerms[0 + LEN_OF_FACULTY_TABLE * x : LEN_OF_FACULTY_TABLE + LEN_OF_FACULTY_TABLE * x]) 
                if state == 'YEAH'.encode('utf-8'):
                    dbQuery.save()
                    user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                else:
                    errorExist = True
                    returnListItem = fileTerms[0 + LEN_OF_FACULTY_TABLE * x : LEN_OF_FACULTY_TABLE + LEN_OF_FACULTY_TABLE * x];
                    returnListItem.append(state)
                    errorImport.append(returnListItem)
            addIsDone = True
            form = FacultyForm(initial={'college' : userCollege})
        elif request.FILES.get('file'):  # dealing with upload
            fileLocation = request.FILES.get('file')
            fileTerms = re.split(',|\n', fileLocation.read())
            multiAdd = True
            terms = []
            for x in range(0, len(fileTerms) / LEN_OF_FACULTY_TABLE):
                    terms.append(
                        fileTerms[0 + x * LEN_OF_FACULTY_TABLE: LEN_OF_FACULTY_TABLE + x * LEN_OF_FACULTY_TABLE])
        else:  # regular form submit
            form = FacultyForm(request.POST)
            if form.is_valid():
                info = form.cleaned_data
                dbQuery = Faculty_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college'],
                    major = info['major'],
                    degree = info['degree'],
                    title = info['title'],
                    isSpecial = info['isSpecial'],
                    photo = info['photo']
                )
                dbQuery.save()
                user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                if dbQuery.isSpecial:
                    if info['canManageCourses']:
                        perm = Permission.objects.get(codename='course_manage')
                        user.user_permissions.add(perm)
                    if info['canManageStudents']:
                        perm = Permission.objects.get(codename='student_manage')
                        user.user_permissions.add(perm)
                    if info['canManageFaculties']:
                        perm = Permission.objects.get(codename='faculty_manage')
                        user.user_permissions.add(perm)
                addIsDone = True
                form = FacultyForm(initial={'college' : userCollege})
        return render(request, 'AddFaculty.html', locals())
    return render(request, 'AccessFault.html')

@login_required
@csrf_exempt
def facultyDelete(request):
    errors = []
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    response = render(request, 'DeleteFaculty.html', locals())
    if request.method == 'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if userCollege != 'all':
                    faculties = Faculty_user.objects.filter(college = userCollege)
                else:
                    faculties = Faculty_user.objects.all()
                response = render(request, 'DeleteFaculty.html', locals())
            else:
                faculties = getSearchResult(searchType, searchTerm, userCollege, 'FACULTY')
                response = render(request, 'DeleteFaculty.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
            return response
        elif 'deleteid' in request.POST:
            facultyId = request.POST.get('deleteid')
            Faculty_user.objects.filter(id = facultyId).delete()
            User.objects.filter(id = facultyId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType  ==   'id':
                    facultiesTemp = Faculty_user.objects.filter(id = searchTerm)
                    faculties = []
                    for faculty in facultiesTemp:
                        faculties.append(faculty)
                elif searchType  ==   'name':
                    facultiesTemp = Faculty_user.objects.filter(name__icontains = searchTerm)
                    faculties = []
                    for faculty in facultiesTemp:
                        faculties.append(faculty)
            response = render(request, 'DeleteFaculty.html', locals())
            return response
        else:
            return response
    return render(request, 'AccessFault.html')

@login_required
def facultyModify(request):
    errors = []
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if userCollege != 'all':
                    faculties = Faculty_user.objects.filter(college = userCollege)
                else:
                    faculties = Faculty_user.objects.all()
            else:
                faculties = getSearchResult(searchType, searchTerm, userCollege, 'FACULTY')
            return render(request, 'ModifyFaculty.html', locals())
        elif 'modifyid' in request.POST:
            inModify = True
            facultyId = request.POST.get('modifyid')
            term = Faculty_user.objects.filter(id = facultyId)
            form = FacultyFormModify(initial = {
                'id': facultyId,
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college,
                'major': term[0].major,
                'degree': term[0].degree,
                'title': term[0].title}
                )
            return render(request, 'ModifyFaculty.html', locals())
        else:
            form = FacultyFormModify(request.POST)
            if form.is_valid():
                info = form.cleaned_data

                user = Faculty_user.objects.get(id=info['id'])
                user.contact = info['contact']
                user.name = info['name']
                user.gender = info['gender']
                user.college = info['college']
                user.major = info['major']
                user.degree = info['degree']
                user.title = info['title']
                user.save()

                modifyIsDone = True
            return render(request, 'ModifyFaculty.html', locals())
    return render(request, 'AccessFault.html')

@login_required
def studentAdd(request):
    errors = []
    errorImport = []
    addIsDone = False
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    isSuper = False
    if userCollege == 'all':
        isSuper = True

    if request.method  ==   'POST':
        if request.POST.get('multiAddCancle') or request.POST.get('first'): #click cancle button or first access
                form = StudentForm(initial = {'college' : userCollege})
        elif 'file' in request.POST and len(request.POST.get('file')) > 0:  # click confirm button
            fileTerms = re.split(',', request.POST.get('file'))
            for x in range(0, len(fileTerms) / LEN_OF_STUDENT_TABLE):
                dbQuery = Student_user(
                    id = fileTerms[0 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    contact = fileTerms[1 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    name = fileTerms[2 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    gender = fileTerms[3 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    college = fileTerms[4 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    major = fileTerms[5 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    grade = fileTerms[6 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    gpa = fileTerms[7 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                    credits = fileTerms[8 + LEN_OF_STUDENT_TABLE * x].encode('utf-8')
                )
                state = importStudentCheck(fileTerms[0 + LEN_OF_STUDENT_TABLE * x : LEN_OF_STUDENT_TABLE + LEN_OF_STUDENT_TABLE * x])
                if state == 'YEAH'.encode('utf-8'):
                    user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                    dbQuery.save()
                else:
                    errorExist = True
                    returnListItem = fileTerms[0 + LEN_OF_STUDENT_TABLE * x : LEN_OF_STUDENT_TABLE + LEN_OF_STUDENT_TABLE * x]
                    returnListItem.append(state)
                    errorImport.append(returnListItem)
            addIsDone = True
            form = StudentForm(initial = {'college' : userCollege})
        elif request.FILES.get('file'):  # dealing with upload
            fileLocation = request.FILES.get('file')
            fileTerms = re.split(',|\n', fileLocation.read())
            multiAdd = True
            terms = []
            for x in range(0, len(fileTerms) / LEN_OF_STUDENT_TABLE):
                terms.append(
                    fileTerms[0 + x * LEN_OF_STUDENT_TABLE: LEN_OF_STUDENT_TABLE + x * LEN_OF_STUDENT_TABLE])
        else:  # regular form submit
            form = StudentForm(request.POST)
            if form.is_valid():
                info = form.cleaned_data
                dbQuery = Student_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college'],
                    major = info['major'],
                    grade = info['grade'],
                    gpa = info['gpa'],
                    credits = info['credits'],
                    isSpecial = info['isSpecial'],
                    photo = info['photo']
                )
                dbQuery.save()
                user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                if dbQuery.isSpecial:
                    if info['canManageCourses']:
                        perm = Permission.objects.get(codename='course_manage')
                        user.user_permissions.add(perm)
                    if info['canManageStudents']:
                        perm = Permission.objects.get(codename='student_manage')
                        user.user_permissions.add(perm)
                    if info['canManageFaculties']:
                        perm = Permission.objects.get(codename='faculty_manage')
                        user.user_permissions.add(perm)
                addIsDone = True
                form = StudentForm(initial = {'college' : userCollege})
        return render(request, 'AddStudent.html', locals())
    return render(request, 'AccessFault.html')

@login_required
@csrf_exempt
def studentDelete(request):
    errors = []
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    response = render(request, 'DeleteStudent.html', locals())
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if userCollege != 'all':
                    students = Student_user.objects.filter(college = userCollege)
                else:
                    students = Student_user.objects.all()
                response = render(request, 'DeleteStudent.html', locals())
            else:
                students = getSearchResult(searchType, searchTerm, userCollege, 'STUDENT')
                response = render(request, 'DeleteStudent.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
            return response
        elif 'deleteid' in request.POST:
            studentId = request.POST.get('deleteid')
            Student_user.objects.filter(id = studentId).delete()
            User.objects.filter(username = studentId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType == 'id':
                    studentsTemp = Student_user.objects.filter(id = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.append(student)
                elif searchType  ==   'name':
                    studentsTemp = Student_user.objects.filter(name__icontains = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.append(student)
            response = render(request, 'DeleteStudent.html', locals())
            return response
        else:
            return response
    return render(request, 'AccessFault.html')

@login_required
def studentModify(request):
    errors = []
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if userCollege != 'all':
                    students = Student_user.objects.filter(college = userCollege)
                else:
                    students = Student_user.objects.all()
            else:
                students = getSearchResult(searchType, searchTerm, userCollege, 'STUDENT')
            return render(request, 'ModifyStudent.html', locals())
        elif 'modifyid' in request.POST:
            inModify = True
            studentId = request.POST.get('modifyid')
            term = Student_user.objects.filter(id = studentId)
            form = StudentFormModify(initial = {
                'id': studentId,
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college,
                'major': term[0].major,
                'grade': term[0].grade,
                'gpa': term[0].gpa,
                'credits' : term[0].credits}
                )
            return render(request, 'ModifyStudent.html', locals())
        else:
            form = StudentFormModify(request.POST)
            if form.is_valid():
                info = form.cleaned_data

                user = Student_user.objects.get(id=info['id'])
                user.contact = info['contact']
                user.name = info['name']
                user.gender = info['gender']
                user.college = info['college']
                user.major = info['major']
                user.grade = info['grade']
                user.gpa = info['gpa']
                user.credits = info['credits']
                user.save()

                modifyIsDone = True
            return render(request, 'ModifyStudent.html', locals())
    return render(request, 'AccessFault.html')

@login_required
@permission_required('IMS.admin_manage')
def adminAdd(request):
    errors = []
    errorImport = []
    existed = []
    addIsDone = False

    if request.method == 'POST':
        if request.POST.get('multiAddCancel') or request.POST.get('first'): #click cancle button or first access
            form = AdminForm()
        elif 'file' in request.POST and len(request.POST.get('file')) > 0:  # click confirm button
            fileTerms = re.split(',', request.POST.get('file'))
            for x in range(0, len(fileTerms) / LEN_OF_FACULTY_TABLE):
                dbQuery = Admin_user(
                    id = fileTerms[0 + LEN_OF_ADMIN_TABLE * x].encode('utf-8'),
                    contact = fileTerms[1 + LEN_OF_ADMIN_TABLE * x].encode('utf-8'),
                    name = fileTerms[2 + LEN_OF_ADMIN_TABLE * x].encode('utf-8'),
                    gender = fileTerms[3 + LEN_OF_ADMIN_TABLE * x].encode('utf-8'),
                    college = fileTerms[4 + LEN_OF_ADMIN_TABLE * x].encode('utf-8'),
                )
                state = importAdminCheck(fileTerms[0 + LEN_OF_ADMIN_TABLE * x : LEN_OF_ADMIN_TABLE + LEN_OF_ADMIN_TABLE * x])
                if state == 'YEAH'.encode('utf-8'):
                    dbQuery.save()
                    user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                else:
                    errorExist = True
                    returnListItem = fileTerms[0 + LEN_OF_ADMIN_TABLE * x : LEN_OF_ADMIN_TABLE + LEN_OF_ADMIN_TABLE * x];
                    returnListItem.append(state)
                    errorImport.append(returnListItem)
            addIsDone = True
            form = FacultyForm()
        elif request.FILES.get('file'):  # dealing with upload
            fileLocation = request.FILES.get('file')
            fileTerms = re.split(',|\n', fileLocation.read())
            multiAdd = True
            terms = []
            for x in range(0, len(fileTerms) / LEN_OF_ADMIN_TABLE):
                    terms.append(
                        fileTerms[0 + x * LEN_OF_ADMIN_TABLE: LEN_OF_ADMIN_TABLE + x * LEN_OF_ADMIN_TABLE])
        else:  # regular form submit
            form = AdminForm(request.POST)
            if form.is_valid():
                info = form.cleaned_data
                dbQuery = Admin_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college']
                )
                dbQuery.save()
                user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                perm1 = Permission.objects.get(codename='student_manage')
                perm2 = Permission.objects.get(codename='faculty_manage')
                perm3 = Permission.objects.get(codename='course_manage')
                user.user_permissions.add(perm1, perm2, perm3)
                if dbQuery.college == 'all':
                    perm = Permission.objects.get(codename='admin_manage')
                    user.user_permissions.add(perm)
                addIsDone = True
                form = AdminForm()
        return render(request, 'AddAdmin.html', locals())
    return render(request, 'AccessFault.html')

@login_required
@csrf_exempt
@permission_required('IMS.admin_manage')
def adminDelete(request):
    errors = []
    userCollege = ""
    if Admin_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    elif Faculty_user.objects.filter(id = request.user.username):
        userCollege = Admin_user.objects.filter(id = request.user.username)[0].college
    else:
        userCollege = Student_user.objects.filter(id = request.user.username)[0].college
    response = render(request, 'DeleteAdmin.html', locals())
    if request.method == 'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if userCollege != 'all':
                    admins = Admin_user.objects.filter(college = userCollege)
                else:
                    admins = Admin_user.objects.all()
                response = render(request, 'DeleteAdmin.html', locals())
            else:
                admins = getSearchResult(searchType, searchTerm, userCollege, 'ADMIN')
                response = render(request, 'DeleteAdmin.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
            return response
        elif 'deleteid' in request.POST:
            adminId = request.POST.get('deleteid')
            Admin_user.objects.filter(id = adminId).delete()
            User.objects.filter(id = adminId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType  ==   'id':
                    adminTemp = Admin_user.objects.filter(id = searchTerm)
                    admins = []
                    for admin in adminTemp:
                        admins.append(admin)
                elif searchType  ==   'name':
                    adminTemp = Admin_user.objects.filter(name__icontains = searchTerm)
                    admins = []
                    for admin in adminTemp:
                        admins.append(admin)
            response = render(request, 'DeleteAdmin.html', locals())
            return response
        else:
            return response
    return render(request, 'AccessFault.html')

@login_required
@permission_required('IMS.admin_manage')
def adminModify(request):
    errors = []
    if request.method == 'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            admins = Admin_user.objects.all()
            return render(request, 'ModifyAdmin.html', locals())
        elif 'modifyid' in request.POST:
            inModify = True
            adminId = request.POST.get('modifyid')
            term = Admin_user.objects.filter(id = adminId)
            form = AdminFormModify(initial = {
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college}
                )
            return render(request, 'ModifyAdmin.html', locals())
        else:
            form = AdminFormModify(request.POST)
            if form.is_valid():
                info = form.cleaned_data

                user = Admin_user.objects.get(id=info['id'])
                user.contact = info['contact']
                user.name = info['name']
                user.gender = info['gender']
                user.college = info['college']
                user.save()

                modifyIsDone = True
            return render(request, 'ModifyAdmin.html', locals())
    return render(request, 'AccessFault.html')