from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout  
from  datetime  import  *  
import time
from django.http import HttpResponseRedirect
from classChoose.login import *

# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.template import loader,Context
from classChoose.models import *
from time import strftime,localtime
import json
from django.views.decorators.csrf import csrf_protect
class PageHeader:
	sid=1
	sname=' '
	cid=1
	cname=' '
	credit=0.1
	college=' '
	smajor=' '

class Classes:
	teacherName=' '
	classTime1=1
	classTime2=2
	classRoom=' '
	capacity=0
@login_required(login_url="/login/")  
def search_form(request):
	forcelogout(request)
    return render_to_response('search_form.html')

@login_required(login_url="/login/")  
def choose_class(request):
	forcelogout(request)
	a = ""
	if request.method == 'POST':
		a = request.POST.get('hiddenInput','')
		pageheader=PageHeader( )
		class_list=[]
		List3=[]
		List4=[]
		#a = "success"
		#分离字符串
		tem=[]
		tem=a.split('#')
		a1=''
		del tem[len(tem)-1]
		Csuccess=1
		if 'xh' in request.GET:
			xh = request.GET['xh']
		if 'xkkh' in request.GET:
			xkkh = request.GET['xkkh']

			HavenClass = Class_table.objects.filter(student=xh)
			for Eachclass in HavenClass:
				if Eachclass.Class.course.id==xkkh:
					Eachclass.delete()
			for temp in tem:
				classes1 = Class_info.objects.get(id=temp)
				HavenClass = Class_table.objects.filter(student=xh)
				student=Student_user.objects.get(id=xh)
				#对每一门课程 检验是否冲突
				for Eachclass in HavenClass:
					#eachclass=Class_info.objects.get(id=EachClass.Class)
					#上课时间冲突，非同一门课 的话
					if classes1.time==Eachclass.Class.time and classes1.course.id!=Eachclass.Class.course.id:
						Csuccess=2
					#考试时间冲突，非同一门课
					if classes1.examtime==Eachclass.Class.examtime and Eachclass.Class.examdate==classes1.examdate and  classes1.course.id!=Eachclass.Class.course.id:
						Csuccess=3
					if classes1.id==Eachclass.Class.id:
						Csuccess=4
				#对于每一门课程注册
				if  Csuccess==1:
					q=Class_table(id=classes1.id+student.id,Class=classes1,student=student,status=0)
					q.save()
					a='%r class choose success' % classes1.teacher.name
				if Csuccess==2:
					a='%r  class time error' % classes1.teacher.name
				if Csuccess==3:
					a='%r class exam time error' % classes1.teacher.name
				if Csuccess==4:
					a='%r class Already have' % classes1.teacher.name
				a1=a1+a

			student = Student_user.objects.get(id=xh)
			course = Course_info.objects.get(id=xkkh)
			classes = Class_info.objects.filter(course=xkkh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.cid=course.id
			pageheader.cname=course.name
			pageheader.credit=course.credits
			#for i in range(0, 1 + 1):
			for class_listing in classes:
				class_dict={}
				class_dict['teacherName']=class_listing.teacher.name
				class_dict['classTime1']=course.semester
				class_dict['classTime2']=class_listing.time
				class_dict['classRoom']=class_listing.room
				class_dict['capacity']=class_listing.capacity
				class_dict['jId']=class_listing.id
				class_list.append(class_dict)
				List3.append(class_listing.id)
			#message = 'You submitted an empty form.%r' % tem
			HavenClass = Class_table.objects.filter(student=xh)
			for Eachclass in HavenClass:
				if Eachclass.Class.course.id:
					List4.append(Eachclass.Class.id)

			return render_to_response('classchoose.html',{'pageHeader':pageheader,'classes':class_list,'List':json.dumps(List3),'flag': a1,'List2':json.dumps(List4)},context_instance=RequestContext(request))
			#return HttpResponse(message)
	else:
		pageheader=PageHeader( )
		class_list=[]
		List3=[]
		List4=[]
		if 'xh' in request.GET:
			xh = request.GET['xh']
		if 'xkkh' in request.GET:
			xkkh = request.GET['xkkh']
			student = Student_user.objects.get(id=xh)
			course = Course_info.objects.get(id=xkkh)
			classes = Class_info.objects.filter(course=xkkh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.cid=course.id
			pageheader.cname=course.name
			pageheader.credit=course.credits
			#for i in range(0, 1 + 1):
			for class_listing in classes:
				class_dict={}
				class_dict['teacherName']=class_listing.teacher.name
				class_dict['classTime1']=course.semester
				class_dict['classTime2']=class_listing.time
				class_dict['classRoom']=class_listing.room
				class_dict['capacity']=class_listing.capacity
				class_dict['jId']=class_listing.id
				class_list.append(class_dict)
				List3.append(class_listing.id)
			HavenClass = Class_table.objects.filter(student=xh)
			for Eachclass in HavenClass:
				if Eachclass.Class.course.id==xkkh:
					List4.append(Eachclass.Class.id)
			#message = 'You submitted an empty form.%r' % class_list[0]['teacherName']
			return render_to_response('classchoose.html',{'pageHeader':pageheader,'classes':class_list,'List':json.dumps(List3),'List2':json.dumps(List4)},context_instance=RequestContext(request))
			
@login_required(login_url="/login/")  
def show_class(request):
	forcelogout(request)
	a = ""
	if request.method == 'POST':
		a = request.POST.get('hiddenInput','')
		pageheader=PageHeader( )
		class_list=[]
		List3=[]
		List4=[]
		#a = "success"
		#分离字符串
		tem=[]

		tem=a.split('#')

		year3=tem[0]
		#temyear=year.split('-')
		sem=tem[1]
		#message = 'You submitted an empty form.%r' % year3
		#return HttpResponse(message)
		sem.encode('gbk')
		#print (year3)
		#message = 'You submitted an empty form.%r' % tem[0]
		#return HttpResponse(message)
		year_first=year3[0]+year3[1]+year3[2]+year3[3]
		year_second=year3[4]+year3[5]+year3[6]+year3[7]
		
		year=year_first+'-'+year_second
		
		sem1=sem[0]
		sem=int(sem)
		sem1=int(sem1)
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.college=student.college
			pageheader.smajor=student.major
			choose=Class_table.objects.filter(student=xh)
			for class_listing in choose:
				#class_listing=Class_info.objects.get(id=Eachclass.Class.id)
				if class_listing.Class.year==year and (class_listing.Class.course.semester==sem or class_listing.Class.course.semester==(sem%10) or class_listing.Class.course.semester==sem1):
					eachcourse=Course_info.objects.get(id=class_listing.Class.course.id)
					class_dict={}
					class_dict['cID']=class_listing.Class.id
					class_dict['className']=eachcourse.name
					class_dict['teacherName']=class_listing.Class.teacher.name

					if eachcourse.semester==1:
						class_dict['classSem']='spring'
					if eachcourse.semester==2:
						class_dict['classSem']='summer'
					if eachcourse.semester==3:
						class_dict['classSem']='fall'
					if eachcourse.semester==4:
						class_dict['classSem']='winner'
					if eachcourse.semester==12:
						class_dict['classSem']='spring/summer'
					if eachcourse.semester==34:
						class_dict['classSem']='fall/winner'
					class_dict['classTime']=class_listing.Class.time
					class_dict['classRoom']=class_listing.Class.room
					class_dict['status']=class_listing.status
					class_dict['teachingStyle']=eachcourse.style
					class_list.append(class_dict)
			#message = 'You submitted an empty form.%d' % sem1
			#return HttpResponse(message)
			return render_to_response('showclass.html',{'pageHeader':pageheader,'classes':class_list,'year1':year3,'sem1':sem})
			#message = 'You submitted an empty form.%r' % month2
			#return HttpResponse(message)
	else:
		pageheader=PageHeader( )
		class_list=[]
		List3=[]
		year1=strftime("%Y",localtime())
		month1=strftime("%m",localtime())
		month2=int(month1,10)
		year2=int(year1,10)
		if month2<9:
			year=str(year2-1)+'-'+str(year2)
			#year = "20142015"
			year3=str(year2-1)+str(year2)
			sem='12'
		else:
			year=str(year2)+'-'+str(year2+1)
			year3=str(year2-1)+str(yesr2)
			#year = "20142015"
			sem='34'
		#year=year.decode('utf-8')
		#print year
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.college=student.college
			pageheader.smajor=student.major
			choose=Class_table.objects.filter(student=xh)
			for class_listing in choose:
				#class_listing=Class_info.objects.get(id=Eachclass.Class.id)
				if class_listing.Class.year==year and (class_listing.Class.course.semester==12 or class_listing.Class.course.semester==1 or class_listing.Class.course.semester==2):
					eachcourse=Course_info.objects.get(id=class_listing.Class.course.id)
					class_dict={}
					class_dict['cID']=class_listing.Class.id
					class_dict['className']=eachcourse.name
					class_dict['teacherName']=class_listing.Class.teacher.name
					
					if eachcourse.semester==1:
						class_dict['classSem']='spring'
					if eachcourse.semester==2:
						class_dict['classSem']='summer'
					if eachcourse.semester==3:
						class_dict['classSem']='fall'
					if eachcourse.semester==4:
						class_dict['classSem']='winner'
					if eachcourse.semester==12:
						class_dict['classSem']='spring/summer'
					if eachcourse.semester==34:
						class_dict['classSem']='fall/winner'
					class_dict['classTime']=class_listing.Class.time
					class_dict['classRoom']=class_listing.Class.room
					class_dict['status']=class_listing.status
					class_dict['teachingStyle']=eachcourse.style
					class_list.append(class_dict)
			return render_to_response('showclass.html',{'pageHeader':pageheader,'classes':class_list,'year1':year3,'sem1':sem})
			#message = 'You submitted an empty form.%r' % month2
			#return HttpResponse(message)