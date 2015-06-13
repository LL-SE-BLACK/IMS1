__author__ = 'John'

from django import forms
from IMS.models import Faculty_user, Student_user

class FacultyForm(forms.Form):
    id = forms.CharField(max_length=6)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=20)
    title = forms.CharField(max_length=20)

def clean_faculty_id(self):
	addedFacultyID = self.cleaned_data['id']
	if Faculty_user.objects.filter(id = addedFacultyID):
		raise forms.ValidationError('Faculty number existed!')
	return addedFacultyID

class FacultyFormModify(forms.Form):
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=20)
    title = forms.CharField(max_length=20)

class StudentForm(forms.Form):
    id = models.CharField(max_length=10)
    contact = models.CharField(max_length=11)
    name = models.CharField(max_length=20)
    gender = models.BooleanField
    college = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    grade = models.IntegerField
    gpa = models.FloatField
    credits = models.FloatField

def clean_student_id(self):
    addedStudentID = self.cleaned_data['id']
    if Faculty_user.objects.filter(id = addedStudentID):
        raise forms.ValidationError('Student number existed!')
    return addedStudentID
