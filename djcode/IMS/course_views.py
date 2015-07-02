# -*- coding: utf-8 -*-
__author__ = 'saltless'

import re
import os

from models import Class_info, Course_info,Student_user, Faculty_user, Admin_user
from course_forms import CourseForm, CourseFormModify, CourseFormFacultyAdd, CourseFormFacultyModify

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission


LEN_OF_COURSE_TABLE = 7

@login_required
def courseMain(request):
    canAdd = True
    canDel = True
    canMod = True
    if Admin_user.objects.filter(id = request.user.username):
        return render(request, 'CourseMain.html', locals())
    else:
        userInfo = Faculty_user.objects.filter(id = request.user.username)
        if userInfo:
            if userInfo[0].isSpecial:
                if not request.user.has_perm("IMS.course_manage"):
                    canAdd, canDel, canMod = False, False, False
                return render(request, 'CourseMain.html', locals())
            else :
                return render(request, 'AccessFault.html')
        else:
            userInfo = Student_user.objects.filter(id = request.user.username)
            if userInfo[0].isSpecial:
                if not request.user.has_perm("IMS.course_manage"):
                    canAdd, canDel, canMod = False, False, False
                return render(request, 'CourseMain.html', locals())
            else :
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

def importCheck(term, isAdmin, isFaculty, userCollege):
    if Course_info.objects.filter(course_id = term[0]): #test duplicate add
        return 'ALREADY EXIST'
    if isFaculty and (not userCollege == term[5]):
        return 'DIFF COLLEGE'
    if len(term[0]) > 8:
        return 'ID: TOO LONG'
    if len(term[1]) > 110:
        return 'NAME: TOO LONG'
    if (isDigit(term[2]) != 'FLOAT') and (isDigit(term[2]) != 'INT'):
        return 'CREDITS: FLOAT REQUIRED'
    if isDigit(term[3]) != 'INT':
        return 'SEMESTER: INT REQUIRED'
    if len(term[4]) > 110:
        return 'TEXTBOOK: TOO LONG'
    if len(term[5]) > 50:
        return 'COLLEGE: TOO LONG'
    if isDigit(term[6]) != 'INT':
        return 'TYPE: INT REQUIRED'
    return 'YEAH'

def getSearchResult(searchType, searchTerm, isAdmin, isFaculty, userCollege):
    if searchType == "course_id":
        coursesTemp = Course_info.objects.filter(course_id = searchTerm)
    if searchType == "course_name":
        coursesTemp = Course_info.objects.filter(name__icontains = searchTerm)
    if searchType == "credits":
        coursesTemp = Course_info.objects.filter(credits = searchTerm)
    if searchType == "semester":
        coursesTemp = Course_info.objects.filter(semester = searchTerm)
    if searchType == "textbook":
        coursesTemp = Course_info.objects.filter(textbook = searchTerm)
    if searchType == "college":
        coursesTemp = Course_info.objects.filter(college = searchTerm)
    if searchType == "course_type":
        coursesTemp = Course_info.objects.filter(course_type = searchTerm)
    courses = []
    for course in coursesTemp:
        if isAdmin:
            courses.append(course)
        elif isFaculty and (userCollege == course.college):
            courses.append(course)
    return courses

@login_required
def courseAdd(request):
    errors = []
    errorImport = []
    addIsDone = False
    #===========USER GROUP CHECK========================================================#
    isAdmin = False 																#
    isFaculty = False 																#
    userName = request.user.username 												#
    if Admin_user.objects.filter(id = userName): 									#
        userInfo = Admin_user.objects.filter(id = userName)							#
        if userInfo[0].college == 'all':											#
            isAdmin = True															#
            userCollege = -1														#
        else: 																		#
            isFaculty = True 														#
            userCollege = userInfo[0].college 										#
    elif Faculty_user.objects.filter(id = userName):								#
        userInfo = Faculty_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
    elif Student_user.objects.filter(id = userName):								#
        userInfo = Student_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
        #isAdmin = True																	#
        #isFaculty = False																#
        #userCollege = -1																#
        #============END OF GROUP CHECK=====================================================#
    if request.method == 'POST':
        if request.POST.get('multiAddCancle') or request.POST.get('first'): #click cancle button or first access
            if isAdmin:
                form = CourseForm()
            if isFaculty:
                facultyAdd = True
                form = CourseFormFacultyAdd()
        elif 'file' in request.POST and len(request.POST.get('file')) > 0: #click confirm button
            fileTerms = re.split(',', request.POST.get('file'))
            for x in xrange(0, len(fileTerms) / LEN_OF_COURSE_TABLE):
                dbQuery = Course_info(
                    course_id = fileTerms[0 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    name = fileTerms[1 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    credits = fileTerms[2 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    semester = fileTerms[3 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    textbook = fileTerms[4 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    college = fileTerms[5 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                    course_type = fileTerms[6 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
                )
                state = importCheck(fileTerms[0 + LEN_OF_COURSE_TABLE * x : LEN_OF_COURSE_TABLE * (x + 1)], isAdmin, isFaculty, userCollege)
                if state == 'YEAH'.encode('utf-8'):
                    dbQuery.save()
                else:
                    errorExist = True
                    returnListItem = fileTerms[0 + LEN_OF_COURSE_TABLE * x : LEN_OF_COURSE_TABLE * (x + 1)];
                    returnListItem.append(state)
                    errorImport.append(returnListItem)
            addIsDone = True
            if isAdmin:
                form = CourseForm()
            if isFaculty:
                facultyAdd = True
                form = CourseFormFacultyAdd()
        elif request.FILES.get('file'): #dealing with upload
            fileLocation = request.FILES.get('file')
            fileTerms = re.split(',|\n', fileLocation.read())
            multiAdd = True
            terms = []
            for x in xrange(0, len(fileTerms) / LEN_OF_COURSE_TABLE):
                terms.append(fileTerms[0 + x * LEN_OF_COURSE_TABLE : LEN_OF_COURSE_TABLE + x * LEN_OF_COURSE_TABLE])
        else: #regular form submit
            if isAdmin:
                form = CourseForm(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Course_info(
                        course_id = info['course_id'],
                        name = info['course_name'],
                        credits = info['credits'],
                        semester = info['semester'],
                        textbook = info['textbook'],
                        college = info['college'],
                        course_type = info['course_type'],
                    )
                    dbQuery.save()
                    addIsDone = True
                    form = CourseForm()
            elif isFaculty:
                form = CourseFormFacultyAdd(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Course_info(
                        course_id = info['course_id'],
                        name = info['course_name'],
                        credits = info['credits'],
                        semester = info['semester'],
                        textbook = info['textbook'],
                        college = userCollege,
                        course_type = info['course_type'],
                    )
                    dbQuery.save()
                    addIsDone = True
                    facultyAdd = True
                    form = CourseFormFacultyAdd()
        return render(request, 'AddCourse.html', locals())
    return render(request, 'AccessFault.html')

@login_required
def courseDelete(request):
    errors = []
    #===========USER GROUP CHECK========================================================#
    isAdmin = False 																#
    isFaculty = False 																#
    userName = request.user.username 												#
    if Admin_user.objects.filter(id = userName): 									#
        userInfo = Admin_user.objects.filter(id = userName)							#
        if userInfo[0].college == 'all':											#
            isAdmin = True															#
            userCollege = -1														#
        else: 																		#
            isFaculty = True 														#
            userCollege = userInfo[0].college 										#
    elif Faculty_user.objects.filter(id = userName):								#
        userInfo = Faculty_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
    elif Student_user.objects.filter(id = userName):								#
        userInfo = Student_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
        #isAdmin = True																	#
        #isFaculty = False																#
        #userCollege = -1																#
        #============END OF GROUP CHECK=====================================================#
    response = render(request, 'DeleteCourse.html', locals())
    if request.method == 'POST':
        if 'term' in request.POST:
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if isAdmin:
                    courses = Course_info.objects.all()
                elif isFaculty:
                    courses = Course_info.objects.filter(college = userCollege)
                response = render(request, 'DeleteCourse.html', locals())
            else:
                courses = getSearchResult(searchType, searchTerm, isAdmin, isFaculty, userCollege)
                response = render(request, 'DeleteCourse.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
            return response
        elif 'deleteid' in request.POST:
            courseId = request.POST.get('deleteid')
            Course_info.objects.filter(course_id = courseId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType == 'course_id':
                    coursesTemp = Course_info.objects.filter(course_id = searchTerm)
                    courses = []
                    for course in coursesTemp:
                        if isAdmin:
                            courses.append(course)
                        elif isFaculty and (userCollege == course.college):
                            courses.append(course)
                elif searchType == 'course_name':
                    coursesTemp = Course_info.objects.filter(name__icontains = searchTerm)
                    courses = []
                    for course in coursesTemp:
                        if isAdmin:
                            courses.append(course)
                        elif isFaculty and (userCollege == course.college):
                            courses.append(course)
            response = render(request, 'DeleteCourse.html', locals())
            return response
        else:
            return response
    return render(request, 'AccessFault.html')

@login_required
def courseModify(request):
    errors = []
    #===========USER GROUP CHECK========================================================#
    isAdmin = False 																#
    isFaculty = False 																#
    userName = request.user.username 												#
    if Admin_user.objects.filter(id = userName): 									#
        userInfo = Admin_user.objects.filter(id = userName)							#
        if userInfo[0].college == 'all':											#
            isAdmin = True															#
            userCollege = -1														#
        else: 																		#
            isFaculty = True 														#
            userCollege = userInfo[0].college 										#
    elif Faculty_user.objects.filter(id = userName):								#
        userInfo = Faculty_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
    elif Student_user.objects.filter(id = userName):								#
        userInfo = Student_user.objects.filter(id = userName)						#
        if userInfo[0].isSpecial and request.user.has_perm("IMS.course_manage"):	#
            isFaculty = True														#
            userCollege = userInfo[0].college 										#
        #isAdmin = True																	#
        #isFaculty = False																#
        #userCollege = -1																#
        #============END OF GROUP CHECK=====================================================#
    if request.method == 'POST':
        if 'term' in request.POST: #search box
            inSearch = True
            searchTerm = request.POST.get('term')
            searchType = request.POST.get('type')
            if not searchTerm:
                if isAdmin:
                    courses = Course_info.objects.all()
                elif isFaculty:
                    courses = Course_info.objects.filter(college = userCollege)
            else:
                courses = getSearchResult(searchType, searchTerm, isAdmin, isFaculty, userCollege)
            return render(request, 'ModifyCourse.html', locals())
        elif 'modifyid' in request.POST: #initial info page
            inModify = True
            courseId = request.POST.get('modifyid')
            term = Course_info.objects.filter(course_id = courseId)
            if isAdmin:
                form = CourseFormModify(initial = {
                'course_name': term[0].name,
                'credits': term[0].credits,
                'semester': term[0].semester,
                'textbook': term[0].textbook,
                'college': term[0].college,
                'course_type' : term[0].course_type
                })
            elif isFaculty:
                facultyModify = True
                form = CourseFormFacultyModify(initial = {
                'course_name': term[0].name,
                'credits': term[0].credits,
                'semester': term[0].semester,
                'textbook': term[0].textbook,
                'course_type' : term[0].course_type
                })
            return render(request, 'ModifyCourse.html', locals())
        else: #DB update after press submit on initial info page
            if isAdmin:
                form = CourseFormModify(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Course_info(
                        course_id = request.POST.get('courseId'),
                        name = info['course_name'],
                        credits = info['credits'],
                        semester = info['semester'],
                        textbook = info['textbook'],
                        college = info['college'],
                        course_type = info['course_type'],
                    )
                    dbQuery.save()
                    modifyIsDone = True
            elif isFaculty:
                form = CourseFormFacultyModify(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Course_info(
                        course_id = request.POST.get('courseId'),
                        name = info['course_name'],
                        credits = info['credits'],
                        semester = info['semester'],
                        textbook = info['textbook'],
                        college = userCollege,
                        course_type = info['course_type'],
                    )
                    dbQuery.save()
                    modifyIsDone = True
            return render(request, 'ModifyCourse.html', locals())
    return render(request, 'AccessFault.html')
