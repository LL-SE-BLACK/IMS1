# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Question(models.Model):
    QuestionId = models.CharField(max_length=20)
    Stem = models.CharField(max_length=2000)
    OptionA = models.CharField(max_length=100,blank=True)
    OptionB = models.CharField(max_length=100,blank=True)
    OptionC = models.CharField(max_length=100, blank=True)
    OptionD = models.CharField(max_length=100, blank=True)
    Type = models.IntegerField(null=True)  # 1 choose 3- judge 1. 单选 2 , 多选 3. 判断
    Difficulty = models.IntegerField(null=True) # 1-5 integer
    Flag = models.IntegerField(null=True) #whether modify flag
    Answer = models.CharField(max_length=20)
    Chapter = models.IntegerField()
    CourseId = models.CharField(max_length=8,null=True)
    Score = models.IntegerField(null=True)

class Paper(models.Model):
    PaperId = models.CharField(max_length=20)
    PaperName = models.CharField(max_length=30)
    QId = models.CharField(max_length=400)
    Creator = models.CharField(max_length=20)  #TEAACHER'S id
    ClassId = models.CharField(max_length=10)
    StartTime = models.DateTimeField(null=True)
    Deadline = models.DateTimeField(null=True)
    MaxScore = models.FloatField(null=True)
    MinScore = models.FloatField(null=True)
    SumScore = models.FloatField(null=True)
    SubmitNum = models.IntegerField(null=True)
    Full = models.FloatField(null=True)
# database below is used to analyze
class Score(models.Model):
    StudentId = models.CharField(max_length=20,)
    PaperId = models.CharField(max_length=20,)
    ValidScore = models.FloatField(null=True,)
    SubmitTimes = models.IntegerField(null=True,)
# Used to Analysis
class History(models.Model):
    PaperId = models.CharField(max_length=20)
    QuestionId = models.CharField(max_length=10,null=True)
    QIdError = models.IntegerField(null=True)

class MyAuth(models.Model):
    UserId = models.CharField(max_length = 20,primary_key =True)
    OnAuthClassId = models.CharField(max_length=10)