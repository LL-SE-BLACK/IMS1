from django.db import models

# Create your models here.

#class Login_info: handled by Django User

class Student_user(models.Model):
    '''
    | id | contact | name | gender | college | major | grade | gpa | credits |
    |---|---|---|---|---|---|---|---|---|
    | CHARACTER(10) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | INTEGER | FLOAT | FLOAT |
    '''
    id = models.CharField(max_length=10, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    grade = models.IntegerField
    gpa = models.FloatField
    credits = models.FloatField

class Faculty_user(models.Model):
    '''
    | id | contact | name | gender | college | major | degree | title |
    |---|---|---|---|---|---|---|---|
    | CHARACTER(6) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | VARCHAR(20) | VARCHAR(20) |
    '''
    id = models.CharField(max_length=6, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    degree = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

#class Admin_user: disabled temporarily

class Course_info(models.Model):
    '''
    | course_id | name | credits | semester | textbook | college |
    |---|---|---|---|---|---|
    | CHARACTER(8) | VARCHAR(110) | FLOAT | INTEGER | VARCHAR(110) | VARCHAR(50) |
    '''
    course_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=110)
    credits = models.FloatField
    semester = models.IntegerField
    textbook = models.CharField(max_length=110)
    college = models.CharField(max_length=50)

class Class_info(models.Model):
    '''
    | class_id | course_id | teacher | time | room | examdate | examtime | examroom | capacity |
    |---|---|---|---|---|---|---|---|---|
    | CHARACTER(10) | CHARACTER(8) | VARCHAR(20) | INTEGER | VARCHAR(20) | DATETIME(TEXT) | INTEGER | VARCHAR(20) | INTEGER |
    '''
    class_id = models.CharField(max_length=10)
    course_id = models.CharField(max_length=8)
    teacher = models.CharField(max_length=20)
    time = models.IntegerField
    room = models.CharField(max_length=20)
    examdate = models.DateTimeField
    examtime = models.IntegerField
    examroom = models.CharField(max_length=20)
    capacity = models.IntegerField

class Pre_requisites(models.Model):
    '''
    | id | prereq |
    |---|---|
    | CHARACTER(8) | CHARACTER(8) |
    '''
    courseid = models.CharField(max_length=8)
    prereq = models.CharField(max_length=8)
