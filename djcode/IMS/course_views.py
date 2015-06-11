# -*- coding: utf-8 -*-
__author__ = 'saltless'

import re
import os

from models import Class_info, Course_info
from course_forms import CourseForm, CourseFormModify

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission

LEN_OF_COURSE_TABLE = 6

def courseMain(request):
	return render(request, 'CourseMain.html')

def courseAdd(request):
	if not request.user.is_anonymous():
		return render(request, 'CourseMain.html')
	else:
		errors = []
		existed = []
		addIsDone = False
		if request.method == 'POST':
			if 'file' in request.POST and len(request.POST.get('file')) > 0: #click confirm button
				fileTerms = re.split(',', request.POST.get('file'))
				s = ""
				for x in xrange(0, len(fileTerms) / LEN_OF_COURSE_TABLE):
					dbQuery = Course_info(
						course_id = fileTerms[0 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
						name = fileTerms[1 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
						credits = fileTerms[2 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
						semester = fileTerms[3 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
						textbook = fileTerms[4 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
						college = fileTerms[5 + LEN_OF_COURSE_TABLE * x].encode('utf-8'),
					)
					if Course_info.objects.filter(course_id = fileTerms[0 + LEN_OF_COURSE_TABLE * x]): #test duplicate add
						s = s + str(x)
						isExist = True
						existed.append(fileTerms[0 + x * LEN_OF_COURSE_TABLE : LEN_OF_COURSE_TABLE + x * LEN_OF_COURSE_TABLE])
					else:
						dbQuery.save()
				addIsDone = True
				form = CourseForm()
			elif request.FILES.get('file'): #dealing with upload
				fileLocation = request.FILES.get('file')
				fileTerms = re.split(',|\n', fileLocation.read())
				multiAdd = True
				terms = []
				for x in xrange(0, len(fileTerms) / LEN_OF_COURSE_TABLE):
					terms.append(fileTerms[0 + x * LEN_OF_COURSE_TABLE : LEN_OF_COURSE_TABLE + x * LEN_OF_COURSE_TABLE])
			elif request.POST.get('multiAddCancle'): #click cancle button
				form = CourseForm()
			else: #regular form submit
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
					)
					dbQuery.save()
					addIsDone = True
					form = CourseForm()
		else: #raw form
			form = CourseForm()
		return render(request, 'AddCourse.html', locals())

def courseDelete(request):
	errors = []
	response = render(request, 'DeleteCourse.html', locals())
	if request.method == 'GET':
		if 'term' in request.GET:
			inSearch = True
			searchTerm = request.GET.get('term')
			searchType = request.GET.get('type')
			if not searchTerm:
				errors.append('Please enter a key word')
				response = render(request, 'DeleteCourse.html', locals())
			else:
				if searchType == 'course_id':
					courses = Course_info.objects.filter(course_id = searchTerm)
				elif searchType == 'course_name':
					courses = Course_info.objects.filter(name__icontains = searchTerm)
				#else:
					#courses = Course_info.objects.filter(teacher = searchTerm)
				response = render(request, 'DeleteCourse.html', locals())
				response.set_cookie('deleteTerm', searchTerm)
				response.set_cookie('deleteType', searchType)
	elif request.method == 'POST':
		if 'deleteid' in request.POST:
			courseId = request.POST.get('deleteid')
			Course_info.objects.filter(course_id = courseId).delete()
			isDeleted = True
			if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
				searchTerm = request.COOKIES['deleteTerm']
				searchType = request.COOKIES['deleteType']
				if searchType == 'course_id':
					courses = Course_info.objects.filter(course_id = searchTerm)
				elif searchType == 'course_name':
					courses = Course_info.objects.filter(name__icontains = searchTerm)
			response = render(request, 'DeleteCourse.html', locals())
	return response

def courseModify(request):
	errors = []
	if request.method == 'GET':
		if 'term' in request.GET:
			inSearch = True
			searchTerm = request.GET.get('term')
			searchType = request.GET.get('type')
			if not searchTerm:
				errors.append('Please enter a key word')
			else:
				if searchType == 'course_id':
					courses = Course_info.objects.filter(course_id = searchTerm)
				elif searchType == 'course_name':
					courses = Course_info.objects.filter(name__icontains = searchTerm)
				#else:
					#courses = Course_info.objects.filter(teacher = searchTerm)
	if request.method == 'POST':
		if 'modifyid' in request.POST:
			inModify = True
			courseId = request.POST.get('modifyid')
			term = Course_info.objects.filter(course_id = courseId)
			form = CourseFormModify(initial = {
				'course_name': term[0].name,
				'credits': term[0].credits,
				'semester': term[0].semester,
				'textbook': term[0].textbook,
				'college': term[0].college}
			)
		else:
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
				)
				dbQuery.save()
				modifyIsDone = True	
	return render(request, 'ModifyCourse.html', locals())

