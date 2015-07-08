from django.db import models

# Create your models here.

class User(models.Model):
	id = models.CharField(primary_key=True,max_length=10)
	password = models.CharField(max_length=20)
	auth = models.IntegerField(default=0)
		
class students_users(models.Model):
	id = models.CharField(primary_key=True,max_length=10)
	contact = models.CharField(max_length=11)
	name = models.CharField(max_length=20)
	gender = models.BooleanField(default=0)
	college = models.CharField(max_length=50)
	major = models.CharField(max_length=50)
	grade = models.IntegerField(default=0)
	gpa = models.FloatField(default=0)
	credits = models.FloatField(default=0) 

	def __str__(self):
		return (self.name)

class faculty_users(models.Model):
	id = models.CharField(primary_key=True,max_length=10)
	contact = models.CharField(max_length=11) 
	name = models.CharField(max_length=20)
	college = models.CharField(max_length=50)
	major = models.CharField(max_length=50)
	degree = models.CharField(max_length=20)
	title = models.CharField(max_length=20)
	introduce = models.CharField(max_length=300)
	def __str__(self):
		return (self.name)

class admin_users(models.Model):
	id = models.CharField(primary_key=True,max_length=10)
	contact = models.CharField(max_length=11) 
	name = models.CharField(max_length=20)
	college = models.CharField(max_length=50)
	def __str__(self):
		return (self.name)

class course_info(models.Model):
	id = models.CharField(primary_key=True,max_length=20)
	name = models.CharField(max_length=100)
	college = models.CharField(max_length=50)
	credits = models.FloatField(default=0)
	semester = models.IntegerField(default=0)
	textbook = models.CharField(max_length=110)
	style = models.IntegerField(default=0)
	introduce = models.CharField(max_length=300)
	def __str__(self):
		return (self.name)

class class_info(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	course = models.ForeignKey(course_info,related_name='class_course')
	teacher = models.ForeignKey(faculty_users)
	time = models.CharField(max_length=20)
	room = models.CharField(max_length=20)
	examdate = models.CharField(max_length=10)
	examtime = models.CharField(max_length=10)
	examroom = models.CharField(max_length=20)
	capacity = models.IntegerField(default=0) 
	remain = models.IntegerField(default=0)
	semester = models.IntegerField(default=0)
	year = models.CharField(max_length=9)
	method = models.CharField(max_length=50)
	def __str__(self):
		return (self.id)

class class_choose_info(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	Class = models.ForeignKey(class_info)
	student = models.ForeignKey(students_users)
	status = models.BooleanField(default=0)
	def __str__(self):
		return (self.id)

class scheme_info(models.Model):
	id = models.CharField(max_length=50,primary_key=True)
	student = models.ForeignKey(students_users)
	course = models.ForeignKey(course_info,related_name='scheme_course')
	state = models.IntegerField(default=0)
	def __str__(self):
		return (self.id)

class choose_time(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	start_time = models.CharField(max_length=50)
	end_time = models.CharField(max_length=50)
	buXuan_start_time = models.CharField(max_length=50)
	buXuan_end_time = models.CharField(max_length=50)

class buXuan_info(models.Model):
	id=models.CharField(max_length=10,primary_key=True)
	student = models.ForeignKey(students_users)
	Class = models.ForeignKey(class_info)
	reason = models.CharField(max_length=300)

class college_demand(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	college = models.CharField(max_length=50)
	majorCourse_demand = models.IntegerField(default=0)
	optionCourse_demand = models.IntegerField(default=0)
	generalCourse_demand = models.IntegerField(default=0)

class pingjia(models.Model):
	id =models.CharField(max_length=10,primary_key=True)
	student = models.ForeignKey(students_users)
	Class = models.ForeignKey(class_info)
	dengji = models.CharField(max_length=10)

class count(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	value = models.IntegerField(default=0)




		









