from django import forms

class sourse_form(forms.Form):
	cr_ID = forms.CharField(max_length=20)
	cr_Name = forms.CharField(max_length=20, required=False)
	cr_Type = forms.CharField(max_length=20, required=False)
	cr_capa = forms.IntegerField(required=False);
	cr_camp = forms.CharField(max_length=20, required=False)
	type = forms.CharField(max_length=10)