from django import forms

class PaperGenerateForm(forms.Form):
  #  Chapter = forms.ModelMultipleChoiceField(choices={'', 'Chapter1', 'chapter2',''})
    SelectNum = forms.IntegerField()
    CheckNum = forms.IntegerField()
    Difficulty = forms.FloatField()
    PaperName = forms.CharField()
    DeadLine = forms.DateTimeField()
    #def clean_

class QuestionSearchForm(forms.Form):
    #Chapter = forms.ModelMultipleChoiceField(widget=,choices=(('0',' '),('1','Chapter1'),('2','chapter2')))
    Difficulty = forms.IntegerField()
    Keyword = forms.CharField()
    DfI = forms.IntegerField()
    DfU = forms.IntegerField()

#CHOICE = (('OptionA','A'),('OptionB','B'),('OptionC','C'),('OptionC','C'))
class CHQuestionAddForm(forms.Form):
    Stem = forms.CharField(max_length=2000)
    #Option = forms.MultipleChoiceField(label=u'', choices=CHOICE, widget=forms.CheckboxSelectMultiple())
    OptionA = forms.CharField()
    OptionAS = forms.ChoiceField(choices=(('null','-----'),('hello',1),('hi',30)))
    OptionB = forms.CharField()
    OptionBS = forms.CheckboxInput()
    OptionC = forms.CharField()
    OptionCS = forms.Select()
    OptionD = forms.CharField()
    OptionDS = forms.Select()
    Score = forms.FloatField()
    Difficulty = forms.IntegerField(max_value=5,min_value=1)
    Chapter = forms.CharField()

class JUQuestionAddForm(forms.Form):
    Stem = forms.CharField()
    OptionA = forms.CharField()
    OptionAS = forms.RadioSelect()
    OptionB = forms.CharField()
    OptionBS = forms.RadioSelect()
    Score = forms.FloatField()
    Difficulty = forms.IntegerField(max_value=5,min_value=1)
    Chapter = forms.CharField()