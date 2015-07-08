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
from classChoose.models import Class_info,Student_user,Course_info,Class_table,choose_time,pingjia,buXuan_info
from time import strftime,localtime
from classChoose.login import *
import http.client
import time
import json

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


def search_form(request):
    return render_to_response('search_form.html')

def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ##print(ltime)
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    ##print(ttime)
    dat="%u%02u%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="%02u%02u%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    return dat+tm
    

    
def choose_class(request):
	a = ""
	#北京时间
	time2=get_webservertime('www.baidu.com')
	#日期
	time3=int(time2)/1000000;

	timeyear=int(time3/10000);
	timemonth=int(time3%10000/100);
	##print timeyear
	##print timemonth
	if timemonth<9:
		timeyear=str(timeyear-1)+'-'+str(timeyear)
		timesem=12
		timesem1=1
		timesem2=2
	else:
		timeyear=str(timeyear)+'-'+str(timeyear+1)
		timesem=34
		timesem1=3
		timesem2=4
	#timeyear=timeyear.decode('utf-8')
	##print timeyear
	##print timesem1
	##print timesem
	##print timesem2	
	if request.method == 'POST':
		#获取当前时间以判断是否是修过的课程
		#year1=strftime("%Y",localtime())
		#month1=strftime("%m",localtime())
		#day1=strftime("%d",localtime())
		#month2=int(month1,10)
		#year2=int(year1,10)
		#if month2<9:
		#	year=str(year2-1)+'-'+str(year2)
	#		sem='12'
		#else:
		#	year=str(year2)+'-'+str(year2+1)
		#	sem='34'
		#year=year.decode('utf-8')
		##print year
		##print sem
		##print month1
		##print day1
		#确定是否在选课时间内,组合成一个int
		#tempp=year1+month1+day1
		#tempp=int(tempp)#表示是否在选课时间内
		##print tempp
		succ1=0;
		timeChoose=choose_time.objects.all()
		#判断是否在选课时间段内
		time2=int(time2)
		for time1 in timeChoose:
			timetpp=time1.start_time.split(' ')
			timetpp1=timetpp[0].split('-')
			timetpp2=timetpp[1].split(':')
			start_time1=timetpp1[0]+timetpp1[1]+timetpp1[2]+timetpp2[0]+timetpp1[1]+timetpp1[2]
			#print (start_time1)

			timetpp=time1.end_time.split(' ')
			timetpp1=timetpp[0].split('-')
			timetpp2=timetpp[1].split(':')
			end_time1=timetpp1[0]+timetpp1[1]+timetpp1[2]+timetpp2[0]+timetpp1[1]+timetpp1[2]

			if time2>int(start_time1) and time2<int(end_time1):
				succ1=1;
		##print succ1

		a = request.POST.get('hiddenInput','')
		pageheader=PageHeader( )
		class_list=[]
		List3=[]
		List4=[]
		#a = "success"
		#分离字符串
		tem=[]
		tem=a.split('#')
		#rint (tem)
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
				#Eachclass.save()
			for temp in tem:
				timecof=0
				classes1 = Class_info.objects.get(id=temp)
				timeclass=classes1.time
				timeclass1=timeclass.split('|')
				week1=[]
				classt1=[]
				for tempclass in timeclass1:
					#分离星期与课程
					temm=tempclass.split('0')
					week=temm[0]
					classt=temm[1]

					week1.append(week)
					classt1.append(classt)
				##print week1
				##print classt1
				HavenClass = Class_table.objects.filter(student=xh)
				student=Student_user.objects.get(id=xh)
				#对每一门课程 检验是否冲突
				for Eachclass in HavenClass:
					#eachclass=Class_info.objects.get(id=EachClass.Class)
					#上课时间冲突，非同一门课 的话
					timeclass=Eachclass.Class.time
					timeclass1=timeclass.split('|')
					for tempclass in timeclass1:
						#分离星期与课程
						temm=tempclass.split('0')
						week=temm[0]
						classt=temm[1]
						for i in range(0,len(week1)-1):
							if week==week1[i] and classt==classt1[i]:
								timecof=1
					if timecof==1 and classes1.course.id!=Eachclass.Class.course.id:
						Csuccess=2
					#考试时间冲突，非同一门课
					if classes1.examtime==Eachclass.Class.examtime and Eachclass.Class.examdate==classes1.examdate and  classes1.course.id!=Eachclass.Class.course.id:
						Csuccess=3
					if classes1.id==Eachclass.Class.id:
						Csuccess=4
				#对于每一门课程注册
				if  Csuccess==1 and succ1==1:
					q=Class_table(id=classes1.id+student.id,Class=classes1,student=student,status=0)
					q.save()
					a='%r class choose success' % classes1.teacher.name
				if Csuccess==2 and succ1==1:
					a='%r  class time error' % classes1.teacher.name
				if Csuccess==3 and succ1==1:
					a='%r class exam time error' % classes1.teacher.name
				if Csuccess==4 and succ1==1:
					a='%r class Already have' % classes1.teacher.name
				if succ1==0:
					a='time error'
				a1=a1+a
			#显示信息头
			student = Student_user.objects.get(id=xh)
			course = Course_info.objects.get(id=xkkh)
			classes = Class_info.objects.filter(course=xkkh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.cid=course.id
			pageheader.cname=course.name
			pageheader.credit=course.credits
			#for i in range(0, 1 + 1):
			#本学期所有课程
			for class_listing in classes:
				
				semyes=(class_listing.semester==timesem or class_listing.semester==timesem1 or class_listing.semester==timesem)
				##print semyes
				if class_listing.year==timeyear and semyes==1:
					class_dict={}
					class_dict['teacherName']=class_listing.teacher.name
					timeclass=class_listing.time
					timeclass1=timeclass.split('|')
					a3=[]
					#classt1=[]
					for tempclass in timeclass1:
						#分离星期与课程
						temm=tempclass.split('0')
						week=temm[0]
						classt=temm[1]
						a4="week %s " %week
						a5="class %s" %classt
						a3.append(a4+a5)
					if class_listing.semester==1:
						class_dict['classTime1']='spring'
					if class_listing.semester==2:
						class_dict['classTime1']='summer'
					if class_listing.semester==3:
						class_dict['classTime1']='fall'
					if class_listing.semester==4:
						class_dict['classTime1']='winner'
					if class_listing.semester==12:
						class_dict['classTime1']='spring/summer'
					if class_listing.semester==34:
						class_dict['classTime1']='fall/winner'
					#class_dict['classTime1']=course.semester
					class_dict['classTime2']=a3
					class_dict['classRoom']=class_listing.room
					class_dict['capacity']=class_listing.capacity
					class_dict['remain']=class_listing.remain
					class_dict['jId']=class_listing.id
					class_list.append(class_dict)
					List3.append(class_listing.id)
			#message = 'You submitted an empty form.%r' % tem
			HavenClass = Class_table.objects.filter(student=xh)
			for Eachclass in HavenClass:
				semyes=(Eachclass.Class.semester == timesem or Eachclass.Class.semester == timesem1 or Eachclass.Class.semester == timesem2)
				if Eachclass.Class.course.id==xkkh and semyes==1 and Eachclass.Class.year==timeyear:
					List4.append(Eachclass.Class.id)

			#List4=['1','2']
			##print List4
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
			print (timeyear)
			for class_listing in classes:
				semyes=(class_listing.semester==timesem or class_listing.semester==timesem1 or class_listing.semester==timesem)
				#将上课时间转化为字符串

				if class_listing.year==timeyear and semyes==1:
					class_dict={}
					class_dict['teacherName']=class_listing.teacher.name
					timeclass=class_listing.time
					timeclass1=timeclass.split('|')
					a3=[]
					#classt1=[]
					for tempclass in timeclass1:
						#分离星期与课程

						temm=tempclass.split('0')
						##print temm
						week=temm[0]
						classt=temm[1]
						a4="week %s " %week
						a5="class %s" %classt
						a3.append(a4+a5)
					if class_listing.semester==1:
						class_dict['classTime1']='spring'
					if class_listing.semester==2:
						class_dict['classTime1']='summer'
					if class_listing.semester==3:
						class_dict['classTime1']='fall'
					if class_listing.semester==4:
						class_dict['classTime1']='winner'
					if class_listing.semester==12:
						class_dict['classTime1']='spring/summer'
					if class_listing.semester==34:
						class_dict['classTime1']='fall/winner'
					#class_dict['classTime1']=course.semester
					class_dict['classTime2']=a3
					class_dict['classRoom']=class_listing.room
					class_dict['capacity']=class_listing.capacity
					class_dict['remain']=class_listing.remain
					class_dict['jId']=class_listing.id
					class_list.append(class_dict)
					List3.append(class_listing.id)
			HavenClass = Class_table.objects.filter(student=xh)
			for Eachclass in HavenClass:
				semyes=(Eachclass.Class.semester == timesem or Eachclass.Class.semester == timesem1 or Eachclass.Class.semester == timesem2)
				if Eachclass.Class.course.id==xkkh and semyes==1 and Eachclass.Class.year==timeyear:
					List4.append(Eachclass.Class.id)
			##print (HavenClass)
			#List3=['1','2']
			#message = 'You submitted an empty form.%r' % class_list[0]['teacherName']
			#List4=['1','2']
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
		##print (year3)
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
		##print year
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

def buxuan(request):
	a=""
	if request.method == 'POST':
		a = request.POST.get('choosereason','')
		##print a
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
		if 'xkkh' in request.GET:
			xkkh = request.GET['xkkh']
			class_dict={}
			choose=Class_info.objects.get(id=xkkh)
			class_dict['name']=choose.course.name
			#判断是否已经补选，是否在补选时间
			time2=get_webservertime('www.baidu.com')
			yibu=0
			tiaojian=xh+xkkh
			buxuan1=buXuan_info.objects.filter(id=tiaojian)
			##print buxuan1
			for eachbu in buxuan1:
				yibu=1
			##print yibu
			succ1=0;
			timeChoose=choose_time.objects.all()
			#判断是否在选课时间段内
			time2=int(time2)
			for time1 in timeChoose:
				timetpp=time1.start_time.split(' ')
				timetpp1=timetpp[0].split('-')
				timetpp2=timetpp[1].split(':')
				start_time1=timetpp1[0]+timetpp1[1]+timetpp1[2]+timetpp2[0]+timetpp1[1]+timetpp1[2]
				timetpp=time1.end_time.split(' ')
				timetpp1=timetpp[0].split('-')
				timetpp2=timetpp[1].split(':')
				end_time1=timetpp1[0]+timetpp1[1]+timetpp1[2]+timetpp2[0]+timetpp1[1]+timetpp1[2]
				print (start_time1)
				print (time1.end_time)
				print (time2)
				if time2>int(start_time1) and time2<int(end_time1):
					succ1=1;
			##print succ1
			if yibu==0 and succ1==1:
				q=buXuan_info(id=xh+xkkh,Class=choose,student=student,reason=a)
				q.save()
				a1='success'
				##print a1
			if succ1==0:
				a1='time error'
			if	yibu==1:
				a1='Already have'
			return render_to_response('chooseextra.html',{'class':class_dict,'flag': a1},context_instance=RequestContext(request))
			#message = 'You submitted an empty form.%r' % a
			#return HttpResponse(message)
				
	else:
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
		if 'xkkh' in request.GET:
			xkkh = request.GET['xkkh']
			class_dict={}
			choose1=Class_info.objects.get(id=xkkh)
			class_dict['name']=choose1.course.name
			return render_to_response('chooseextra.html',{'class':class_dict},context_instance=RequestContext(request))
		
		
def pingjia1(request):
	a=""
	list=[]
	List=[]
	pageheader=PageHeader()
	time2=get_webservertime('www.baidu.com')
	#日期
	time3=int(time2)/1000000;
	##print time3
	timeyear=time3/10000;
	timemonth=time3%10000/100;
	if timemonth<9:
		timeyear=str(timeyear-1)+'-'+str(timeyear)
		timesem=12
		timesem1=1
		timesem2=2
	else:
		timeyear=str(timeyear)+'-'+str(timeyear+1)
		timesem=34
		timesem1=3
		timesem2=4
	#timeyear=timeyear.decode('utf-8')
	if request.method == 'POST':
		a = request.POST.get('hiddenInput','')
		##print a
		a1=a.split('$')
		##print a1
		
		pageheader=PageHeader( )
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
			for i in range(1,len(a1)):
				a2=a1[i].split('#')
				if a2[1]!='Undefined':
					Class1=Class_info.objects.get(id=a2[0])
					q=pingjia(id=xh+a2[0],Class=Class1,student=student,dengji=a2[1])
					q.save()
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.college=student.college
			pageheader.smajor=student.major
			class1=Class_table.objects.filter(student=xh)

			for eachclass in class1:
				already=0
				if timeyear!=eachclass.Class.year:
					already=1
				else:
					if timesem!=eachclass.Class.semester and timesem1!=eachclass.Class.semester and timesem2!=eachclass.Class.semester:
						already=1

				list1={}
				id1=xh+eachclass.id
				yipingjia=pingjia.objects.filter(id=id1)
				yipingjia1=0
				for eachpingja in yipingjia:
					yipingjia1=1
				if yipingjia1==0 and already==1:
					list1['courseName']=eachclass.Class.course.name
					list1['teacherName']=eachclass.Class.teacher.name
					list1['jID']=eachclass.Class.id
					List.append(eachclass.Class.id)
			#	#print list1
					list.append(list1)
			##print list
			##print List
				
			return render_to_response('evaluate.html',{'pageHeader':pageheader,'classes':list,'List':List},context_instance=RequestContext(request))
	else:
		if 'xh' in request.GET:
			xh = request.GET['xh']
			student = Student_user.objects.get(id=xh)
			pageheader.sid=student.id
			pageheader.sname=student.name
			pageheader.college=student.college
			pageheader.smajor=student.major
			class1=Class_table.objects.filter(student=xh)
			#print timeyear
			#print timesem1
			for eachclass in class1:
				list1={}
				id1=xh+eachclass.id
				yipingjia=pingjia.objects.filter(id=id1)
				already=0
				if timeyear!=eachclass.Class.year:
					already=1
				else:
					if timesem!=eachclass.Class.semester and timesem1!=eachclass.Class.semester and timesem2!=eachclass.Class.semester:
						already=1
				
				yipingjia1=0
				
				for eachpingja in yipingjia:
					yipingjia1=1
				if yipingjia1==0 and already==1:
					list1['courseName']=eachclass.Class.course.name
					list1['teacherName']=eachclass.Class.teacher.name
					list1['jID']=eachclass.Class.id
					List.append(eachclass.Class.id)
				##print list1
					list.append(list1)
			##print list
			##print List
			return render_to_response('evaluate.html',{'pageHeader':pageheader,'classes':list,'List':List},context_instance=RequestContext(request))
