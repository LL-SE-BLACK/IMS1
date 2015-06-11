# -*- coding: utf-8 -*-
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
    contact = models.CharField(max_length=11,default='18812345678')
    name = models.CharField(max_length=20,default='张三')
    gender = models.BooleanField(default=True)
    college = models.CharField(max_length=50,default='计算机科学与技术学院')
    major = models.CharField(max_length=50,default='计算机科学与技术')
    grade = models.IntegerField(default=3)
    gpa = models.FloatField(default=4.0)
    credits = models.FloatField(default=100.0)

    def __unicode__(self):
        return u'id:%s, contact:%s, name:%s, gender:%d, college:%s, major:%s, grade:%s, gpa:%f, credits:%f'%(self.id, self.contact,self.name,self.gender, self.college,self.major,self.grade, self.gpa, self.credits)
        # return 'id:' + self.id


class Faculty_user(models.Model):
    '''
    | id | contact | name | gender | college | major | degree | title |
    |---|---|---|---|---|---|---|---|
    | CHARACTER(6) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | VARCHAR(20) | VARCHAR(20) |
    '''
    id = models.CharField(max_length=6, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField(default=0)
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    degree = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

class Admin_user(models.Model):
    '''
    | id | contact | name | gender | college |
    |---|---|---|---|---|
    | CHARACTER(3) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) |
    '''
    id = models.CharField(max_length=3, primary_key=True)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField(default=0)
    college = models.CharField(max_length=50)

class Course_info(models.Model):
    '''
    | course_id | name | credits | semester | textbook | college |
    |---|---|---|---|---|---|
    | CHARACTER(8) | VARCHAR(110) | FLOAT | INTEGER | VARCHAR(110) | VARCHAR(50) |
    '''
    course_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=110)
    credits = models.FloatField(default=0)
    semester = models.IntegerField(default=0)
    textbook = models.CharField(max_length=110)
    college = models.CharField(max_length=50)

class Class_info(models.Model):
    '''
    | class_id | course_id | teacher | time | room | examdate | examtime | examroom | capacity |
    |---|---|---|---|---|---|---|---|---|
    | CHARACTER(10) | CHARACTER(8) | VARCHAR(20) | INTEGER | VARCHAR(20) | DATETIME(TEXT) | INTEGER | VARCHAR(20) | INTEGER |
    '''
    class_id = models.CharField(max_length=10)
    course_id = models.ForeignKey(Course_info)
    teacher = models.CharField(max_length=20)
    time = models.IntegerField(default=0)
    room = models.CharField(max_length=20)
    examdate = models.DateTimeField
    examtime = models.IntegerField(default=0)
    examroom = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)

class Pre_requisites(models.Model):
    '''
    | id | prereq |
    |---|---|
    | CHARACTER(8) | CHARACTER(8) |
    '''
    course_id = models.CharField(max_length=8)
    prereq = models.CharField(max_length=8)

class class_table(models.Model):
    '''
    | student_id | class_id |
    |---|---|
    | CHARACTER(10) | CHARACTER(10) |
    '''
    student_id = models.ForeignKey(Student_user)
    class_id = models.ForeignKey(Class_info)