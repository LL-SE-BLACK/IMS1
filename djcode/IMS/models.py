# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

#class Login_info: handled by Django User
import os
from django.conf import settings
DEFAULT_PHOTO_DIR = os.path.join("photo", "default.jpg")


def get_photo_file_name(instance, filename):
    # print instance.id
    # print filename
    filename = filename.encode('utf-8')
    newFilename = os.path.join("photo", str(instance.id)) + "." + str(filename).split('.')[-1]
    newFullFilename = os.path.join(settings.MEDIA_ROOT, newFilename)
    if os.path.exists(newFullFilename):
        os.remove(newFullFilename)
    return newFilename

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
    isSpecial = models.BooleanField(default=False)
    photo = models.FileField(upload_to=get_photo_file_name, default=DEFAULT_PHOTO_DIR)

    def __unicode__(self):
        return u'id:%s, contact:%s, name:%s, gender:%d, college:%s, major:%s, grade:%s, gpa:%f, credits:%f'%(self.id, self.contact,self.name,self.gender, self.college,self.major,self.grade, self.gpa, self.credits)
        # return 'id:' + self.id

    def __str__(self):
        return self.name


class Faculty_user(models.Model):
    '''
    | id | contact | name | gender | college | major | degree | title |
    |---|---|---|---|---|---|---|---|
    | CHARACTER(6) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) | VARCHAR(50) | VARCHAR(20) | VARCHAR(20) |
    '''
    id = models.CharField(max_length=6, primary_key=True)
    contact = models.CharField(max_length=11, default= "18812345678")
    name = models.CharField(max_length=20,default= "张三")
    gender = models.BooleanField(default=0)
    college = models.CharField(max_length=50,default="计算机科学与技术学院")
    major = models.CharField(max_length=50,default='计算机科学与技术')
    degree = models.CharField(max_length=20,default='博士')
    title = models.CharField(max_length=20, default="研究员")
    isSpecial = models.BooleanField(default=False)
    photo = models.FileField(upload_to=get_photo_file_name, default=DEFAULT_PHOTO_DIR)


    def __unicode__(self):
        return u'id:%s, contact:%s, name:%s, gender:%d, college:%s, major:%s, degree:%s, title:%s'%(self.id, self.contact,self.name,self.gender, self.college,self.major,self.degree, self.title)
        # return 'id:' + self.id

    def __str__(self):
        return self.name

class Admin_user(models.Model):
    '''
    | id | contact | name | gender | college |
    |---|---|---|---|---|
    | CHARACTER(3) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) |
    '''
    id = models.CharField(max_length=3, primary_key=True)
    contact = models.CharField(max_length=11,default="18812345678")
    name = models.CharField(max_length=20, default="张三")
    gender = models.BooleanField(default=0)
    college = models.CharField(max_length=50, default="all") #default for superadmin
    photo = models.FileField(upload_to=get_photo_file_name, default=DEFAULT_PHOTO_DIR)


    def __unicode__(self):
        return u'id:%s, contact:%s, name:%s, gender:%d, college:%s'%(self.id, self.contact,self.name,self.gender, self.college)
        # return 'id:' + self.id

    def __str__(self):
        return self.name

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
    course_type = models.IntegerField(default=0) #必修、选项和通识，根据选课组要求加入

    def __str__(self):
        return self.name

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
    semester = models.IntegerField(default=0) #开课学期
    remain = models.IntegerField(default=0) #选课剩余容量
    year = models.IntegerField(default=2015) #年份（学年）
    language = models.IntegerField(default=0) #中文、英文、双语

    def __str__(self):
        return self.id

class Pre_requisites(models.Model):
    '''
    | id | prereq |
    |---|---|
    | CHARACTER(8) | CHARACTER(8) |
    '''
    course_id = models.CharField(max_length=8)
    prereq = models.CharField(max_length=8)

class Class_table(models.Model):
    '''
    | student_id | class_id |
    |---|---|
    | CHARACTER(10) | CHARACTER(10) |
    '''
    student_id = models.ForeignKey(Student_user)
    class_id = models.ForeignKey(Class_info)

class Sys_log(models.Model):
    time = models.CharField(max_length=20)
    optype = models.CharField(max_length=20, default='update')
    table = models.CharField(max_length=20)
    primkey = models.CharField(max_length=20)
    field = models.CharField(max_length=20)
    pre = models.CharField(max_length=50, default='none')
    post = models.CharField(max_length=50, default='none')