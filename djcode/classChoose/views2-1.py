# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
from chooseCourse.models import *
from django.views.decorators.csrf import csrf_protect
import json
import xlwt

def first_page(request):
    return HttpResponse("<p> 你好 </p>")
	
@csrf_protect 	
def templay(request):
	#get the student's ID
	user_id = request.GET['id']
	print("id = " + user_id)
	
	#use ID to get student's info
	user_info = Student_user.objects.get(id=user_id)
	Student_info = {'name': user_info.name,'id': user_info.id, 'college': user_info.college, 'major': user_info.major}
	credit = {}
	
	flag = ""
	if request.method=='POST':
		#get the POST TOKEN
		flag = request.POST.get('hiddenInput','')
		
		#split the selected course
		list_new = flag.split('A')
		list_new.pop()
		
		#add the new selected course
		for e in list_new:
			temp = user_id+ "_" + e
			try:
			#是否由此记录
				scheme_info.objects.get(id=temp)
			except:
				scheme_info.objects.create(id=temp, student_id=user_id, course_id=e)
		
		#get the course list
		list_required = Course_info.objects.filter(style=0, college=user_info.college)
		list_optional = Course_info.objects.filter(style=1, college=user_info.college)
		list_common = Course_info.objects.filter(scheme_course__student__id=user_info.id, style=2)
		
		#get all course list
		list_all = list_required | list_optional
		all = []
		for e in list_all:
			all.append(e.id)
		
		#delete the courses cancelled by the student
		list_deleted = scheme_info.objects.filter(student_id=user_id).exclude(course__style=2)
		print(list_deleted.values())
		for e in list_new:
			print(e)
			list_deleted = list_deleted.exclude(course_id=e)
			print(list_deleted.values())
		for e in list_deleted:
			scheme_info.objects.get(id=e.id).delete()
		
		#Calculate the credits
		selected_required = list_required.filter(scheme_course__student__id=user_id)
		total_required = 0
		for e in selected_required:
			total_required = total_required + e.credits
		selected_optional = list_optional.filter(scheme_course__student__id=user_id)
		total_optional = 0
		for e in selected_optional:
			total_optional = total_optional + e.credits
		total_common = 0
		for e in list_common:
			total_common = total_common + e.credits
		credit = {'necessary1': 32, 'necessary2': total_required, 'alter1': 41,\
		'alter2': total_optional, 'common1': 34, 'common2': total_common}
		
		#get the new selected courses
		list_selected = scheme_info.objects.filter(student_id=user_id).exclude(course__style=2)
		selected = []
		for e in list_selected:
			selected.append(e.course_id)
		
		flag = '修改成功！'
		#render
		return render(request, 'training plan4.html', {'student': Student_info, 'necessary': list_required,\
		'alter': list_optional, 'common': list_common, 'flag': flag, 'List2': json.dumps(selected),\
		'List': json.dumps(all), 'credit': credit})
	
	else:
		#get the course list
		list_required = Course_info.objects.filter(style=0, college=user_info.college)
		list_optional = Course_info.objects.filter(style=1, college=user_info.college)
		list_common = Course_info.objects.filter(scheme_course__student__id=user_info.id, style=2)
		
		#Calculate the credits
		selected_required = list_required.filter(scheme_course__student__id=user_id)
		total_required = 0
		for e in selected_required:
			total_required = total_required + e.credits
		selected_optional = list_optional.filter(scheme_course__student__id=user_id)
		total_optional = 0
		for e in selected_optional:
			total_optional = total_optional + e.credits
		total_common = 0
		for e in list_common:
			total_common = total_common + e.credits
		credit = {'necessary1': 32, 'necessary2': total_required, 'alter1': 41,\
		'alter2': total_optional, 'common1': 34, 'common2': total_common}
		
		#get all course
		list_all = list_required | list_optional
		all = []
		for e in list_all:
			all.append(e.id)
		
		#get original selected courses
		list_selected = scheme_info.objects.filter(student_id=user_id).exclude(course__style=2)
		selected = []
		for e in list_selected:
			selected.append(e.course_id)
						
		#render
		return render(request, 'training plan4.html', {'student': Student_info, 'necessary': list_required,\
		'alter': list_optional, 'common': list_common, 'flag': flag, 'List2': json.dumps(selected),\
		'List': json.dumps(all), 'credit': credit})
	
@csrf_protect 	
def search(request):
	user_id = request.GET['id']
	print("id = " + user_id)
	
	post_get = ""
	#use ID to get student's info
	user_info = Student_user.objects.get(id=user_id)
	
	search_list = []
	
	List = []
	
	all = []
	
	if request.method=='POST':
		#get the POST TOKEN
		post_get = request.POST.get('hiddenInput','')
		list_get = post_get.split('#')
		
		#clear the search list
		search_list = []
		
		#get the post style
		style = list_get[0]
		del list_get[0]
		
		#if request is search
		if style == "SEARCH":
			#search through course name
			if list_get[0] == "1":
				filter_list = Class_info.objects.filter(course__name__contains=list_get[1])
			#search through course ID
			elif list_get[0] == "2":
				filter_list = Class_info.objects.filter(course__id__contains=list_get[1])
			#search through teacher name
			elif list_get[0] == "3":
				filter_list = Class_info.objects.filter(teacher__name__contains=list_get[1])
			
			all = []
			
			#get the search list
			for e in filter_list:
				temp_list = Course_info.objects.get(id=e.course_id)
				temp_teacherName = e.teacher.name
				temp_classId = e.course_id
				temp_className = temp_list.name
				temp_classSem = temp_list.semester
				temp_classTime = e.time
				temp_classroom = e.room
				temp_classCredit = temp_list.credits
				temp = {'teacherName': temp_teacherName, 'classId': temp_classId, 'className': temp_className,\
				'classSem': temp_classSem, 'classTime': temp_classTime, 'classroom': temp_classroom,\
				'classCredit': temp_classCredit}
				search_list.append(temp)
				all.append(e.course_id)
		
		
		
		#if request is add
		elif style == "ADD":
			all_list = Class_info.objects.all()
		
			all = []
			#get the search list
			for e in all_list:
				try:
					temp_list = Course_info.objects.get(id=e.course_id)
					temp_teacherName = e.teacher.name
					temp_classId = e.course_id
					temp_className = temp_list.name
					temp_classSem = temp_list.semester
					temp_classTime = e.time
					temp_classroom = e.room
					temp_classCredit = temp_list.credits
					temp = {'teacherName': temp_teacherName, 'classId': temp_classId, 'className': temp_className,\
					'classSem': temp_classSem, 'classTime': temp_classTime, 'classroom': temp_classroom,\
					'classCredit': temp_classCredit}
					search_list.append(temp)
					all.append(e.course_id)
				except:
						print("暂无开课")
		
			for e in list_get:
				try:
					temp = user_id + "_" + e
					scheme_info.objects.create(id=temp, student_id=user_id, course_id=e)
				except:
					print("重复选择！")
		
		return render(request, 'courseSearch2.html', {'classes': search_list, 'List': json.dumps(all), 'studentId': user_id})
					
	else:
		all_list = Class_info.objects.all()
		
		all = []
		#get the search list
		for e in all_list:
			try:
				temp_list = Course_info.objects.get(id=e.course_id)
				temp_teacherName = e.teacher.name
				temp_classId = e.course_id
				temp_className = temp_list.name
				temp_classSem = temp_list.semester
				temp_classTime = e.time
				temp_classroom = e.room
				temp_classCredit = temp_list.credits
				temp = {'teacherName': temp_teacherName, 'classId': temp_classId, 'className': temp_className,\
				'classSem': temp_classSem, 'classTime': temp_classTime, 'classroom': temp_classroom,\
				'classCredit': temp_classCredit}
				search_list.append(temp)
				all.append(e.course_id)
			except:
					print("暂无开课")
		
		return render(request, 'courseSearch2.html', {'classes': search_list, 'List': json.dumps(all), 'studentId': user_id})

		
@csrf_protect 	
def show_students(request):
	teacher_id = request.GET['id']
	
	teacher_info = Faculty_users.objects.get(id=teacher_id)
	
	cnum = Class_info.objects.filter(teacher__name=teacher_info.name).count()
	pageHeader = {'tid': teacher_id, 'name': teacher_info.name, 'cnum': cnum}
	
	teacher_class = Class_info.objects.filter(teacher__name=teacher_info.name)
	
	all = []
	#get the search list
	for e in teacher_class:
		try:
			temp_list = Course_info.objects.get(class_course__id=e.id)
			temp_className = temp_list.name
			temp_classSem = temp_list.semester
			temp_classTime = e.time
			temp_classroom = e.room
			temp = {'courseName': temp_className, 'classTime1': temp_classSem, 'classTime2': temp_classTime,\
			'classRoom': temp_classroom, 'jId': e.id}
			all.append(temp)
		except:
			print("暂无开课")
	
	return render(request, 'exportExcel1.html', {'classes': all, 'pageHeader': pageHeader})

	
	
@csrf_protect 	
def download(request):
	teacher_id = request.GET['jsgh']
	class_id = request.GET['jxbid']
	
	print(class_id)
	list = Class_table.objects.filter(Class=class_id)
	
	print(list.values())
	
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Sheetname')
	
	ws.write(0, 0, '学生学号')
	ws.write(0, 1, '联系方式')
	ws.write(0, 2, '姓名')
	ws.write(0, 3, '性别')
	ws.write(0, 4, '学院')
	ws.write(0, 5, '专业')
	ws.write(0, 6, '年级')
	#ws.write(0, 7, '')
	
	i = 1
	
	for e in list:
		print(e.student_id)
		student_list = Student_user.objects.get(id = e.student_id)
		ws.write(i, 0, student_list.id)
		ws.write(i, 1, student_list.contact)
		ws.write(i, 2, student_list.name)
		ws.write(i, 3, student_list.gender)
		ws.write(i, 4, student_list.college)
		ws.write(i, 5, student_list.major)
		ws.write(i, 6, student_list.grade)
		i = i + 1
	
	filename = 'list_' + class_id + '.xls'

	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] ='attachment; filename=%s' % filename
	
	wb.save(response)
	return response
		
		
	
	
	
	
	
	