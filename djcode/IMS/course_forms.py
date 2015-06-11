# -*- coding: utf-8 -*-
__author__ = 'saltless'

from django import forms
from models import Class_info, Course_info

class CourseForm(forms.Form):
	course_id = forms.CharField(max_length = 8)
	course_name = forms.CharField(max_length = 110)
	credits = forms.FloatField()
	semester = forms.IntegerField()
	textbook = forms.CharField(max_length = 110)
	college = forms.CharField(max_length = 50)

	def clean_course_id(self):
		addedCouseID = self.cleaned_data['course_id']
		if Course_info.objects.filter(course_id = addedCouseID):
			raise forms.ValidationError('Course number existed!')
		return addedCouseID

class CourseFormModify(forms.Form):

	course_name = forms.CharField(max_length = 110)
	credits = forms.FloatField()
	semester = forms.IntegerField()
	textbook = forms.CharField(max_length = 110)
	college = forms.CharField(max_length = 50)
