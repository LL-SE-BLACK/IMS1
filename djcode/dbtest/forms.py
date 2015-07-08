from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)