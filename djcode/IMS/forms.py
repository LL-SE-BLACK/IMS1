# -*- coding: utf-8 -*-
from django import forms

class StudentInfoForm(forms.Form):
    id = forms.CharField(max_length=10)
    contact = forms.CharField(max_length=11,default='18812345678')
    name = forms.CharField(max_length=20,default='张三')
    gender = forms.BooleanField(default=True)
    college = forms.CharField(max_length=50,default='计算机科学与技术学院')
    major = forms.CharField(max_length=50,default='计算机科学与技术')
    grade = forms.IntegerField(default=3)
    gpa = forms.FloatField(default=4.0)
    credits = forms.FloatField(default=100.0)

    def clean_message(self):
        pass
