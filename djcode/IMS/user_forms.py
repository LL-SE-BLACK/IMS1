__author__ = 'John'

from django import forms
from IMS.models import Faculty_user, Student_user

class FacultyForm(forms.Form):
    faculty_id = forms.CharField(max_length=6)
    faculty_contact = forms.CharField(max_length=11)
    faculty_name = forms.CharField(max_length=20)
    faculty_gender = forms.BooleanField
    faculty_college = forms.CharField(max_length=50)
    faculty_major = forms.CharField(max_length=50)
    faculty_degree = forms.CharField(max_length=20)
    faculty_title = forms.CharField(max_length=20)

def clean_faculty_id(self):
	addedFacultyID = self.cleaned_data['faculty_id']
	if Faculty_user.objects.filter(faculty_id = addedFacultyID):
		raise forms.ValidationError('Faculty number existed!')
	return addedFacultyID

class FacultyFormModify(forms.Form):
    faculty_contact = forms.CharField(max_length = 11)
    faculty_name = forms.CharField(max_length = 20)
    faculty_gender = forms.BooleanField
    faculty_college = forms.CharField(max_length = 50)
    faculty_major = forms.CharField(max_length = 50)
    faculty_degree = forms.CharField(max_length = 20)
    faculty_title = forms.CharField(max_length = 20)
