# -*- coding: utf-8 -*-
from django import forms

class StudentInfoForm(forms.Form):
    id = forms.CharField(max_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.IntegerField()
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    grade = forms.IntegerField()
    gpa = forms.FloatField()
    credits = forms.FloatField()

    def clean_id(self):
        id = self.cleaned_data['id']
        if len(id) != 10 and not str(id).isdigit():
            raise forms.ValidationError("学号为10位数字!")
        return id

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if not str(contact).isdigit():
            raise forms.ValidationError("电话号码为纯数字!")
        return contact

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender != 1 and gender != 0:
            raise forms.ValidationError("不要干坏事哦！")
        return gender


class FacultyInfoForm(forms.Form):
    id = forms.CharField(max_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.IntegerField()
    college = forms.CharField(max_length=50)
    major = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=20)
    title = forms.CharField(max_length=20)

    def clean_id(self):
        id = self.cleaned_data['id']
        if len(id) != 6 and not str(id).isdigit():
            raise forms.ValidationError("学号为6位数字!")
        return id

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if not str(contact).isdigit():
            raise forms.ValidationError("电话号码为纯数字!")
        return contact

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender != 1 and gender != 0:
            raise forms.ValidationError("不要干坏事哦！")
        return gender

class AdminInfoForm(forms.Form):
    id = forms.CharField(max_length=10)
    contact = forms.CharField(max_length=11)
    name = forms.CharField(max_length=20)
    gender = forms.IntegerField()
    college = forms.CharField(max_length=50)

    def clean_id(self):
        id = self.cleaned_data['id']
        if len(id) != 3 and not str(id).isdigit():
            raise forms.ValidationError("学号为3位数字!")
        return id

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if not str(contact).isdigit():
            raise forms.ValidationError("电话号码为纯数字!")
        return contact

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender != 1 and gender != 0:
            raise forms.ValidationError("不要干坏事哦！")
        return gender


class UserPhotoForm(forms.Form):
    photo = forms.FileField(
        label='Select a file',
        help_text='max. 20 megabytes'
    )

    def clean_photo(self):
        CONTENT_TYPES = ['image']
        MAX_UPLOAD_SIZE = 1024*1024*2 #2M
        photo = self.cleaned_data['photo']
        content_type = photo.content_type.split('/')[0]
        if content_type in CONTENT_TYPES:
            if photo._size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('上传大小限制为20M！')
        else:
            raise forms.ValidationError('请上传图像文件！')

        return photo
