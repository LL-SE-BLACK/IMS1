import json
import time
import itertools
from django.db import models
from models import Faculty_user, classroom, Application, Class_info

class ClassroomSchedule:
	def __init__(self):
		self.initSchedule()

	def initSchedule(self):
		self.schedule = {}
		for i in range(1, 36):
			self.schedule[i] = ""

class TeacherSchedule:
	def __init__(self):
		self.initSchedule()

	def initSchedule(self):
		self.schedule = {}
		for i in range(1, 36):
			self.schedule[i] = ""	

class AutoCourseArrange:
	def __init__(self):
		"""
		initialize
		"""
		#self.arrangeTime = "2015-06-13 15:20:00"
		#self.db = database()
		# classroom model
		self.classroom = classroom.objects.all()
		# application model
		self.application = Application.objects.all()
		# teacher model
		self.teacher = Faculty_user.objects.all()
		print self.teacher
		# init schedules of all classroom
		self.ClassroomSchedule = {}
		for room in self.classroom:
			self.ClassroomSchedule[room.id] = {}
			for i in range(1, 36):
				self.ClassroomSchedule[room.id][i] = ""
		# init schedules of all teachers
		self.TeacherSchedule = {}
		for teac in self.teacher:
			self.TeacherSchedule[teac.id] = {}
			for i in range(1, 36):
				self.TeacherSchedule[teac.id][i] = ""

	def run(self):
		"""
		detect clock repeatedly,
		when it's time to arrange courses,
		begin to arrange.
		"""
		#while (True):
		#	currentTime = self.getCurrentTime()
		#	if currentTime >= self.arrangeTime:
		#		break
		#print "there are ", self.arrange(), "classes arranged"
		self.arrange()
		print self.Schedule
		for i in self.Schedule:
			print i

	def getCurrentTime(self):
		return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

	def arrange(self):
		"""
		arrange course
		simple strategy: when an application fits, arrange it,
		otherwise give up it.
		linear time, better to run several times to get better result.
		"""
		# to save the number of applications that are satisfied
		arranged_classes = 0
		self.Schedule = {}
		#fit every application
		for application in self.application:
			#mapping the classtime to 1 dimension
			classtime = self.transform(application.classTime)
			#fit the application to every classroom
			flag = False	#show if the class is arranged
			#find teacher
			teacher = Faculty_user.objects.get(id = application.teacherID)
			for classroom in self.classroom:
				# if the classroom does not fit the application,
				# turn to another classroom
				if not self.ApplicationFitClassroom(application, classroom):
					continue
				for strategy in itertools.combinations(classtime, application.classHour):
					# if there is no conflict
					if self.FitTime_classroom(strategy, classroom) and self.FitTime_teacher(strategy, teacher):
						self.Schedule[application.id] = {'classroom': classroom.id, 'classTime':[]}
						for k in strategy:
							self.ClassroomSchedule[classroom.id][k] = application.id
							self.TeacherSchedule[teacher.id][k] = application.id
							self.Schedule[application.id]['classTime'].append(k)
							arranged_classes = arranged_classes + 1
						flag = True
						break
				if flag:
					break
		return arranged_classes	

	def ApplicationFitClassroom(self, application, classroom):
		if application.campus!=None and application.campus!=classroom.campus:
			return False
		return True

	def FitTime_classroom(self, timeList, classroom):
		for i in timeList:
			print self.ClassroomSchedule[classroom.id][i]
			if self.ClassroomSchedule[classroom.id][i]!="":
				return False
		return True

	def FitTime_teacher(self, timeList, teacher):
		for i in timeList:
			if self.TeacherSchedule[teacher.id][i]!="":
				return False
		for i in timeList:
			if (i%5==2 or i%5==4):
				if self.TeacherSchedule[teacher.id][i]!="":
					return False
		return True

	def transform(self, class_time):
		"""
		translate applications' class_time into 1 dimension,
		which is easy to deal with.
		"""
		mapping = {
			1:1, 2:1, 3:2, 4:2, 5:2,	# morning 
			6:3, 7:3, 8:3, 9:4, 10:4,	# afternoon
			11:5, 12:5, 13:5	#night
		}
		time_piece = {}
		ClassTime = json.loads(class_time)
		for classtime in ClassTime:
			tmp = (classtime[0]-1) * 5 + mapping[classtime[1]]
			time_piece[tmp] = 1
		ret = time_piece.keys()
		ret.sort()
		return ret
	
	def transform_back(self, class_time):
		"""
		translate applications' class_time into 1 dimension,
		which is easy to deal with.
		"""
		mapping = {
			1:[1, 2], 2:[3,4,5], 3:[6,7,8], 4:[9, 10], 5:[11,12,13],	# morning 
		}
		ret = []
		for i in class_time:
			d = int(i/5)
			if i%5>0:
				d = d+1
			for j in mapping[i - (d-1)*5]:
				ret.append([d, j])
		return json.dumps(ret)

	def Save_Current_Schedule(self):
		for app in self.application:
			if app.id in self.Schedule:
				newClass = Class_info.objects.create(
					course_id = app.cuz_ID,
					teacher = app.teacherID,
					classTime = self.transform_back(self.Schedule[app.id]['classTime']),
					classroom = self.Schedule[app.id]['classroom'],
					capacity = app.class_capacity
					#term = app.term
					)
				newClass.save()