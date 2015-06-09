# -*- coding: utf-8 -*-
from django import forms

class StudentInfoForm(forms.Form):
    id = forms.CharField(max_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField()
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    grade = forms.IntegerField()
    gpa = forms.FloatField()
    credits = forms.FloatField()

    def clean_message(self):
        pass
