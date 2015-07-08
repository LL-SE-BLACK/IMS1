from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout  
from  datetime  import  *  
import time
from django.http import HttpResponseRedirect
from classChoose.login import *

from django.contrib import admin
from django.db.models import Q 
from django.db.models import query
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.contrib.auth.models import User
from classChoose.models import *
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
import random
from django.template import loader
from.models import *
import json
import datetime
#from datetime import datetime
import time 
import threading
# Register your models here.

#@login_required(login_url="/login/")  
def  add_done(class_ID,student_ID):
	#forcelogout(request)
	#提取得到教学班id
	print ("in adding")
	flag=""
	#class_ID = request.POST.get('class_id_hidden')
	#student_ID = request.POST.get('add_id')
	qset = (Q(Class__id = class_ID)&Q(student__id = student_ID))
	n = class_choose_info.objects.filter(qset).count()
	if n==0:
		add_info = class_choose_info()
		Class = class_info.objects.get(id=class_ID)
		print(Class)
		student = students_users.objects.get(id=student_ID)
		print(student)
		#add_info.id = '%d' %(random.randint(1, 100))
		add_info.id = class_ID+student_ID
		add_info.Class = Class     #query class_info by class_id
		add_info.student = student     #query students_users by student_id
		add_info.status = 1
		print (add_info)
		flag = add_info.save()
		print(flag)
		return (flag)
	else:
		choose_info=class_choose_info.objects.get(qset)
		choose_info.status=1
		choose_info.save()
		return (flag)
	

@login_required(login_url="/login/")  
def  delete_done(class_ID,students_ID_list):
	forcelogout(request)
	print ("in deleting")
	flag=True
	#class_ID = request.POST.get('class_id_for_del')
	#students_ID_list = list()
	#student_ID_list = (request.POST.get('hiddenInput')).split('A')
	#print (class_ID)
	#print (student_ID_list[0])
	#提取class_id和student_id(已经选中)
	#delete_info = class_choose_info.objects.filter(class_id=class_ID,student_id=student_ID)
	print (len(students_ID_list))
	for i in range(0,len(students_ID_list)-1):
		qset = (Q(Class__id=class_ID)&Q(student__id=students_ID_list[i]))
		delete_info = class_choose_info.objects.get(qset)
		delete_info.delete()
	if i==len(students_ID_list)-1:
		return (1)
	else:
		return (0)
	#if flag == 1:
		#return HttpResponse('delete success!')
    #else:
    	#return HttpResponse('delete error!')



@login_required(login_url="/login/")  
def select_students_list(class_ID):
	forcelogout(request)
	#print (class_ID)
	#print (class_choose_info.objects.all())
	qset = (Q(Class__id = class_ID)&Q(status = 1))
	choose_list = class_choose_info.objects.filter(qset).order_by('student__id') #class_choose_info和students_users的交集 
	#print (choose_list)
	students_id_list = list()
	students_list = list()
	#print (students_users.objects.all())
	#print (choose_list[0].student.id)
	#print (choose_list.count())
	for choose in choose_list:
		#print ("a")
		#print (choose_list[i].student.id)
		students_id_list.append(choose.student.id)
		students_list.append(students_users.objects.get(id=choose.student.id))
	return (students_list,students_id_list)

@login_required(login_url="/login/")  
def sift(Time,classes_list,admin_college):
	forcelogout(request)
	#time = request.GET['sift_time']
	print("in sifting")
	while 1:
		if  (datetime.datetime.now())>=Time:
			print("It's time now")
			print (class_choose_info.objects.all())
			#print("classes_list:")
			#print (classes_list)
			for Class in classes_list: #for every class
				number = (class_info.objects.get(id=Class.id)).capacity
				qset = (Q(Class__id = Class.id)&Q(status = 0))
				choose_list = class_choose_info.objects.filter(qset)
				if(len(choose_list)==0):  #if no students choose
					break
				else:
					print("Class:")
					print(Class)
					print("number:")
					print(number)
					#print("choose_list:")
					print(choose_list)
					print(len(choose_list)-1)
					if len(choose_list)<=number:     #if choose students less than capacity
						print ("in choose students less than capacity")
						for Choose in choose_list:
							Choose.status=True
							Choose.save()
					else:           #students more than capacity,we use score  to select
						score_list = list()
						print (choose_list)
						for i in range(0,len(choose_list)):
							print ("in for")
							if choose_list[i].student.college==admin_college: #the same college as admin plus 1
								score=2
								if choose_list[i].student.grade==4:        #the last year students plus 1
									score = score+1
								else:
									score = score+0
							else:
								score=0
								if choose_list[i].student.grade==4:        #the last year students plus 1
									score = score+1
								else:
									score = score+0
							print("score")
							print(score)
							score_list.append(score)
						#print(score_list)
						for j in range(0,number): #choose the top number scored students
							print("in choose for")
							Max = score_list[0]
							for Score in score_list:
								if Score > Max:
									Max=Score
							#print("Max:")
							#print (Max)
							index=score_list.index(Max)
							top_choose = choose_list[index]
							print("status:")
							print (top_choose.status)
							top_choose.status=True
							top_choose.save()
							print("status again:")
							print (top_choose.status)
							score_list[index]=0  #except the choosen top ones 
						for Choose in choose_list:   #delete other students' records
							if Choose.status!=True:
								Choose.delete()
						print("sifting finishing")
			break
		    	#siftee = random.sample(Class,(Class.count()-number))
		    	#siftee.delete()
		else:
			print("It's not time")
			time.sleep(60)
			continue



@login_required(login_url="/login/")  
def  admin_index(request):
	forcelogout(request)

	admin1 = admin_users(id="1",contact="123",name="zch",college="123")
	admin1.save()

	student1 = students_users(id="1",contact="123456",name="XiaoMing",gender=0,college="123",major="jisuanji",grade=4,gpa=4.5,credits=99.5)
	student1.save()
	student2 = students_users(id="2",contact="123456",name="XiaoHong",gender=1,college="123",major="jisuanji",grade=2,gpa=4.7,credits=100.5)
	student2.save()
	student3 = students_users(id="3",contact="123456",name="XiaoLi",gender=1,college="1234",major="xindian",grade=4,gpa=4.8,credits=110.5)
	student3.save()

	course1 = course_info(id="1",name="DM",college="123",credits=2.0,semester=1,textbook= 'Data mining',style=1,introduce = "呵呵")
	course1.save()
	course2 = course_info(id="2",name="SE",college="123",credits=2.0,semester=2,textbook= 'Software engineering',style=1)
	course2.save()
	course3 = course_info(id="3",name="QiPa",college="123",credits=4.0,semester=1,textbook= 'QiPa',style=2)
	course3.save()

	teacher1 = faculty_users(id="1",contact="123456",name="CaiDeng",college="123",major="jisuanji",degree="doctor",title="professor")
	teacher1.save()
	teacher2 = faculty_users(id="2",contact="123456",name="ChenYue",college="123",major="jisuanji",degree="doctor",title="professor")
	teacher2.save()

	class1 = class_info(id="1",course=course1,teacher=teacher1,time="3012",room="101",examdate="20150607",examtime="12:21",examroom="101",capacity=60,remain=60,semester=12,year="2014-2015",method="English")
	class1.save()
	class2 = class_info(id="2",course=course1,teacher=teacher2,time="2013",room="102",examdate="20150607",examtime="12:21",examroom="102",capacity=60,remain=60,semester=12,year="2014-2015",method="English")
	class2.save()
	class3 = class_info(id="3",course=course2,teacher=teacher2,time="4012|2012",room="103",examdate="20150608",examtime="16:21",examroom="103",capacity=30,remain=30,semester=34,year="2013-2014",method="English")
	class3.save()
	class4 = class_info(id="4",course=course3,teacher=teacher2,time="4012",room="201",examdate="20151008",examtime="10:30",examroom="201",capacity=2,remain=2,semester=34,year="2013-2014",method="English")
	class4.save()

	#class_choose1 = class_choose_info(id="1",student=student1,Class=class1,status=0)
	#class_choose1.save()
	#class_choose2 = class_choose_info(id="2",student=student2,Class=class2,status=1)
	#class_choose2.save()
	#class_choose3 = class_choose_info(id="3",student=student1,Class=class2,status=1)
	#class_choose3.save()
	#class_choose4 = class_choose_info(id="4",student=student2,Class=class1,status=1)
	#class_choose4.save()
	#class_choose5 = class_choose_info(id="5",student=student2,Class=class3,status=0)
	#class_choose5.save()
	#class_choose6 = class_choose_info(id="180",student=student3,Class=class3,status=0)
	#class_choose6.save()
	class_choose1 = class_choose_info(id="14",student=student1,Class=class4,status=0)
	class_choose1.save()
	class_choose2 = class_choose_info(id="24",student=student2,Class=class4,status=0)
	class_choose2.save()	
	class_choose3 = class_choose_info(id="34",student=student3,Class=class4,status=0)
	class_choose3.save()

	college_demand1 =  college_demand(id="1",college="123",	majorCourse_demand =20 ,optionCourse_demand =20 ,generalCourse_demand = 20)
	college_demand1.save()

	#buXuan_info1= buXuan_info(id="1",student =student1 ,Class =class1 ,reason ="大四狗")
	#buXuan_info1.save()

	#user = User.objects.create_user(username='1',password='1',first_name = "0")
	#user.save 
	#user = User.objects.create_user(username='2',password='2',first_name = "1")
	#user.save 
	#user = User.objects.create_user(username='3',password='3',first_name = "2")
	#user.save 

	count1=count(id="1",value=0)
	count1.save()

	admin_id = request.GET['id']

	if admin_id=="2":
		print ("if")
		return HttpResponse("permission denied!")

	print ("id:"+admin_id)
	admin = admin_users.objects.get(id=admin_id)#the currently loggedin user
	a=False
	if a:
	#if admin.is_authenticated() == False:
		return render(
			request,
			"login.html"
			)
	else:
		admin_college = admin.college
		#course_info = course_info.objects.filter(college=admin_college)
		classes_list = class_info.objects.filter(course__college=admin_college).order_by('-course__id')#本学院的所有课
		#sorted(classes_list)
		#for every class in classes_list 
		#class.remian=class.capacity-(class_choose_info.objects.filter(id=class.id).count())
		#print(classes_list) 
		for Class in classes_list:
			qset = (Q(Class__id = Class.id)&Q(status = 1))
			Class.remain = Class.capacity - (class_choose_info.objects.filter(qset).count())
		#print (classes_list)
		if request.method=='GET':
			return render(
				request,
				"adminpage1.html",
				{'classes':classes_list, 'admin':admin},
			)
		
		else:
			ch_time=choose_time(id="1",	start_time =request.POST.get('start_time') ,end_time =request.POST.get('sift_time') ,buXuan_start_time =request.POST.get('buxuan_time') ,buXuan_end_time = request.POST.get('end_buxuan_time'))
			ch_time.save()
			print (choose_time.objects.all())
			Time = request.POST.get('sift_time')
			time.end_time = Time
			print (Time)
			Time_=datetime.datetime.now()
			Time_= datetime.datetime.strptime(Time,"%Y-%m-%d %H:%M:%S")
			#time = datetime.datetime.strptime(Time,"%Y-%m-%d %H:%M:%S").datetime()
			print(Time_)
			thread1=threading.Thread(target=sift,name="sifter",args=(Time_,classes_list,admin_college))
			thread1.start()
			return render(
				request,
				"adminpage1.html",
				{'classes':classes_list, 'admin':admin},
			)



@login_required(login_url="/login/")  
def  admin_page2(request):
	forcelogout(request)
	class_ID = request.GET.get('class_id')
	#print (students_list)
	#print (students_id_list)
	if request.method == 'GET':	
		#class_ID = request.GET.get('class_id')
		print (class_ID)
		a=""
		(students_list,students_id_list) = select_students_list(class_ID)
		return render(
			request,
			"adminpage2.html",
			{'students':students_list,'List':students_id_list,'flag':a}
			)
	else :
		print ("in POST")
		#class_ID = request.POST.get('class_id_for_del')
		#students_ID_list = list()
		#student_ID_list = (request.POST.get('hiddenInput')).split('A')
		#print (class_ID)
		#print (student_ID_list)
		Tag = request.POST.get('tag')
		print (Tag)
		if Tag == "1":
			print ("haha")
			#class_ID = request.POST.get('class_id_hidden')
			student_ID = request.POST.get('add_id')
			print (student_ID)
			#add_done(Request)
			flag=add_done(class_ID,student_ID)
			(students_list,students_id_list) = select_students_list(class_ID)
			return render(
				request,
				"adminpage2.html",
				{'students':students_list,'List':students_id_list,'flag2':flag}
				)
		else:
			student_IDs = request.POST.get('hiddenInput')
			students_ID_list=list()
			if(student_IDs):
				students_ID_list = student_IDs.split('A')
			print ("class_ID:"+class_ID)
			print (students_ID_list)
			flag=delete_done(class_ID,students_ID_list)
			(students_list,students_id_list) = select_students_list(class_ID)
			return render(
				request,
				"adminpage2.html",
				{'students':students_list,'List':students_id_list,'flag':flag}
				)



@login_required(login_url="/login/")  
def buXuan(request):
	forcelogout(request)
	print ("buXuan")
	class_ID = request.GET.get('class_id')
	Class=class_info.objects.get(id=class_ID)
	cid=class_ID
	cname =Class.course.name

	print (class_ID)
	#class_ID = request.GET.get('class_id')
	#print (students_list)
	#print (students_id_list)
	if request.method == 'GET':	
		#class_ID = request.GET.get('class_id')
		print (class_ID)
		a=""
		buXuan_list = buXuan_info.objects.filter(Class__id = class_ID).order_by('student__id')
		print (buXuan_info.objects.all())
		#(students_list,students_id_list) = select_students_list(class_ID)
		students_id_list=list()
		for buXuan in buXuan_list:
			students_id_list.append(buXuan.student.id)

		return render(
			request,
			"bySelect.html",
			{'buXuan':buXuan_list,'List':students_id_list,'cid':cid,'cname':cname}
			)
	else :                                          #补选添加
		print ("in POST")
		#class_ID = request.POST.get('class_id_for_del')
		#students_ID_list = list()
		#student_ID_list = (request.POST.get('hiddenInput')).split('A')
		#print (class_ID)
		#print (student_ID_list)

		print ("haha")
		#class_ID = request.POST.get('class_id_hidden')
		student_ID = request.POST.get('add_id')[:-1]
		print ("student_ID:")
		print (student_ID)
		#add_done(Request)
		flag=add_done(class_ID,student_ID)
		print ("flag:")
		print (flag)

		
		qset = (Q(Class__id = class_ID)&Q(student__id = student_ID))
		buXuan1=buXuan_info.objects.get(qset)
		buXuan1.delete()
		#(students_list,students_id_list) = select_students_list(class_ID)
		buXuan_list = buXuan_info.objects.filter(Class__id = class_ID).order_by('student__id')
		students_id_list=list()
		for buXuan in buXuan_list:
			students_id_list.append(buXuan.student.id)

		return render(
			request,
			"bySelect.html",
			{'buXuan':buXuan_list,'List':students_id_list,'cid':cid,'cname':cname}
			)



