from django.db import models

# Create your models here.



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




		









