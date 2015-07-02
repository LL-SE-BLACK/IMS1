__author__ = 'Henry'

__author__ = 'John'

from django import forms
from IMS.models import Faculty_user, Student_user, Admin_user, DEFAULT_PHOTO_DIR


class FacultyForm(forms.Form):
    id = forms.CharField(max_length=6, min_length=6)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.CharField(max_length=1)
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=20)
    title = forms.CharField(max_length=20)
    isSpecial = forms.BooleanField(False)
    canManageCourses = forms.BooleanField(False)
    canManageStudents = forms.BooleanField(False)
    canManageFaculties = forms.BooleanField(False)
    photo = forms.FileField(initial = DEFAULT_PHOTO_DIR)

    def clean_id(self):
        addedFacultyID = self.cleaned_data['id']
        if Faculty_user.objects.filter(id = addedFacultyID):
            raise forms.ValidationError('Faculty number existed!')
        return addedFacultyID

    def clean_gender(self):
        addedFacultyGender = self.cleaned_data['gender']
        if addedFacultyGender != 'M' and addedFacultyGender != 'F':
            raise forms.ValidationError('Please input M or F')
        return addedFacultyGender

class FacultyFormModify(forms.Form):
    id = forms.CharField(max_length=6, min_length=6)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField()
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=20)
    title = forms.CharField(max_length=20)

class StudentForm(forms.Form):
    id = forms.CharField(max_length=10, min_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.CharField(max_length=1)
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    grade = forms.IntegerField()
    gpa = forms.FloatField()
    credits = forms.FloatField()
    isSpecial = forms.BooleanField(False)
    canManageCourses = forms.BooleanField(False)
    canManageStudents = forms.BooleanField(False)
    canManageFaculties = forms.BooleanField(False)
    photo = forms.FileField(initial = DEFAULT_PHOTO_DIR)

    def clean_id(self):
        addedStudentID = self.cleaned_data['id']
        if Student_user.objects.filter(id = addedStudentID):
            raise forms.ValidationError('Student number existed!')
        return addedStudentID

    def clean_gender(self):
        addedStudentGender = self.cleaned_data['gender']
        if addedStudentGender != 'M' and addedStudentGender != 'F':
            raise forms.ValidationError('Please input M or F')
        return addedStudentGender

class StudentFormModify(forms.Form):
    id = forms.CharField(max_length=10, min_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField()
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    grade = forms.IntegerField()
    gpa = forms.FloatField()
    credits = forms.FloatField()

class AdminForm(forms.Form):
    '''
    | id | contact | name | gender | college |
    |---|---|---|---|---|
    | CHARACTER(3) | VARCHAR(11) | VARCHAR(20) | BOOLEAN | VARCHAR(50) |
    '''
    id = forms.CharField(max_length=3)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.CharField(max_length = 1)
    college = forms.CharField(max_length=50) #default for superadmin
    photo = forms.FileField(initial=DEFAULT_PHOTO_DIR)

    def clean_id(self):
        addedAdminID = self.cleaned_data['id']
        if Admin_user.objects.filter(id = addedAdminID):
            raise forms.ValidationError('Admin number existed!')
        return addedAdminID

    def clean_gender(self):
        addedAdminGender = self.cleaned_data['gender']
        if addedAdminGender != 'M' and addedAdminGender != 'F':
            raise forms.ValidationError('Please input M or F')
        return addedAdminGender

class AdminFormModify(forms.Form):
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.BooleanField()
    college = forms.CharField(max_length=50)