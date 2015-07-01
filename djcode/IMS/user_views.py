__author__ = 'John'

import re
import os

from models import Class_info, Course_info, Faculty_user, Admin_user, Student_user
from user_forms import StudentForm, FacultyForm, StudentFormModify, FacultyFormModify

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission

LEN_OF_FACULTY_TABLE = 8
LEN_OF_STUDENT_TABLE = 9

@login_required
def userMain(request):
    if Admin_user.objects.filter(id = request.user.username):
        return render(request, 'UserMain.html')
    else:
        return render(request, 'AccessFault.html')

def isDigit(a):
    for x in a:
        if not ((x >= '0' and x <= '9') or x == '.'):
            return False
    pos = a.find('.');
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
        return 'COLLEGE: TOO LONG'   
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

@login_required
def facultyAdd(request):
    errors = []
    errorImport = []
    existed = []
    addIsDone = False                                              

    if request.method == 'POST':
        if request.POST.get('multiAddCancel') or request.POST.get('first'): #click cancle button or first access
            form = FacultyForm()
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
                    isSpecial = fileTerms[8 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
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
            form = FacultyForm()
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
                    isSpecial = info['isSpecial']
                )
                dbQuery.save()
                user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                addIsDone = True
                form = FacultyForm()
        return render(request, 'AddFaculty.html', locals())
    return render(request, 'AccessFault.html')

@login_required
def facultyDelete(request):
    errors = []
    response = render(request, 'DeleteFaculty.html', locals())
    if request.method == 'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                faculties = Faculty_user.objects.all()
                response = render(request, 'DeleteFaculty.html', locals())
            else:
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
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
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
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                faculties = Faculty_user.objects.all()
            else:
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
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
        elif 'modifyid' in request.POST:
            inModify = True
            facultyId = request.POST.get('modifyid')
            term = Faculty_user.objects.filter(id = facultyId)
            form = FacultyFormModify(initial = {
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college,
                'major': term[0].major,
                'degree': term[0].degree,
                'title': term[0].title}
                                     )
        else:
            form = FacultyFormModify(request.POST)
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
                    title = info['title']
                )
                dbQuery.save()
                modifyIsDone = True
            return render(request, 'ModifyFaculty.html', locals())
    return render(request, 'AccessFault.html')

@login_required
def studentAdd(request):
    errors = []
    errorImport = []
    addIsDone = False
        
    if request.method  ==   'POST':
        if request.POST.get('multiAddCancle') or request.POST.get('first'): #click cancle button or first access
                form = StudentForm()
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
            form = StudentForm()
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
                    credits = info['credits']
                )
                dbQuery.save()
                user = User.objects.create_user(dbQuery.id, dbQuery.id+"@zju.edu.cn", "123456")
                addIsDone = True
                form = StudentForm()
        return render(request, 'AddStudent.html', locals())
    return render(request, 'AccessFault.html')

@login_required
def studentDelete(request):
    errors = []
    response = render(request, 'DeleteStudent.html', locals())
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                students = Student_user.objects.all()
                response = render(request, 'DeleteStudent.html', locals())
            else:
                if searchType  ==   'id':
                    studentsTemp = Student_user.objects.filter(id = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
                elif searchType  ==   'name':
                    studentsTemp = Student_user.objects.filter(name__icontains = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
                response = render(request, 'DeleteStudent.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
        elif 'deleteid' in request.POST:
            studentId = request.POST.get('deleteid')
            Student_user.objects.filter(id = studentId).delete()
            User.objects.filter(username = studentId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType  ==   'id':
                    studentsTemp = Student_user.objects.filter(id = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
                elif searchType  ==   'name':
                    studentsTemp = Student_user.objects.filter(name__icontains = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
            response = render(request, 'DeleteStudent.html', locals())
            return response
        else:
            return response
    return render(request, 'AccessFault.html')

@login_required
def studentModify(request):
    errors = []
    if request.method  ==   'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                students = Student_user.objects.all()
            else:
                if searchType  ==   'id':
                    studentsTemp = Student_user.objects.filter(id = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
                elif searchType  ==   'name':
                    studentsTemp = Student_user.objects.filter(name__icontains = searchTerm)
                    students = []
                    for student in studentsTemp:
                        students.appen(student)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
        elif 'modifyid' in request.POST:
            inModify = True
            studentId = request.POST.get('modifyid')
            term = Student_user.objects.filter(id = studentId)
            form = StudentFormModify(initial = {
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
                dbQuery = Student_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college'],
                    major = info['major'],
                    grade = info['grade'],
                    gpa = info['gpa'],
                    credits = info['credits']
                )
                dbQuery.save()
                modifyIsDone = True
            return render(request, 'ModifyStudent.html', locals())
    return render(request, 'AccessFault.html')
