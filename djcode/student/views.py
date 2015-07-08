from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect,Http404
from teacher.models import Paper,Score,Question,Score,History
from IMS.models import Class_info,Student_user,Course_info,Faculty_user,class_table
import re
import datetime
from math import ceil
from django.template.context import RequestContext
from teacher.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission

from django.http import Http404,HttpResponseRedirect,HttpResponse
# Create your views here.
#view all of the course student select

def get_class(request):
    UserId = request.user
    UserClass = MyAuth.objects.get(UserId=UserId)
    return UserClass.OnAuthClassId


def ViewClass(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        StudentId= request.user.username
        ClassTable = class_table.objects.filter(student_id__id=StudentId)
        if not ClassTable:
            return HttpResponse('<html><title></title><body></html>',)
        ClassList = []
        for ClassName in ClassTable:
            ClassId = ClassName.class_id.class_id
            CourseName = ClassName.class_id.course_id.name
            ClassList.append({'Name': CourseName+' '+ClassId,'URL':'/class_list/'+ClassId+'/'})
        return render_to_response('Choose_Class.html',{'ClassList':ClassList},context_instance=RequestContext(request))
    if request.method =='POST':
        try:
            user_class = MyAuth.objects.get(UserId=request.user.username)
            user_class.OnAuthClassId = offset
            user_class.save()
        except MyAuth.DoesNotExist:
            user_class = MyAuth.objects.create(UserId=request.user.username,  OnAuthClassId=offset)

        if len(offset) == 10:
            return HttpResponseRedirect('/student/ViewPaper/')
        else :
            return HttpResponseRedirect('/teacher/AddQuestion/')
# view all paper has been published
def ViewPaper(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method =='GET':
        pagename = 'Online test'
        ClassID = get_class(request)
        now = datetime.datetime.now()
        #start = now-datetime.timedelta(hours=23, minutes=59, seconds=59)
        Paperlist = Paper.objects.filter(ClassId = ClassID,StartTime__lte=now)# add time after starttime
        PaperList =[]
        for paperid in Paperlist:
            #P = Score.objects.filter(StudentId=request.user.username,ClassId=ClassID,PaperId=paperid.PaperId)
            try:
                history = Score.objects.get(StudentId=request.user.username,PaperId = paperid.PaperId)
            except Score.DoesNotExist:
                history=Score.objects.create(StudentId=request.user.username,PaperId = paperid.PaperId,ValidScore=0, SubmitTimes=0)
            paperInfo = {'Full':100,'PaperName':paperid.PaperName,'ValidScore':history.ValidScore,'SubmitTime':history.SubmitTimes,'URL':'/student/test/'+paperid.PaperId+'/','DeadLine':paperid.Deadline}
            PaperList.append(paperInfo)
        return render_to_response('P_viewlist_stu.html',locals(),context_instance=RequestContext(request))

# used to generate question list of a paper
def getquestion(QuesId):
    QuestionIdList = []
    for i in range(20):
        mid = QuesId[i*20:i*20+20]
        QuestionIdList.append(Question.objects.get(QuestionId=mid))
    return  QuestionIdList
#Generate a online test page
def OnlinePaper(request, offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        try:
            Qid = Paper.objects.get(PaperId = offset)
        except Paper.DoesNotExist:
            raise Http404
        student = request.user.username
        Student = Score.objects.get(StudentId=student, PaperId=offset)
        time = Qid.Deadline
        time = time.replace(tzinfo=None)
        if Student.SubmitTimes > 5:
            return HttpResponse('You have reached max submit time!')
        if time<(datetime.datetime.now()):
            return HttpResponse('You have miss the deadline !<br><a href = "/student/ViewPaper/">return to test page</a>')
        QuesId = Qid.QId
        QuestionIdList = getquestion(QuesId)
        URL = '/student/test/score/'+request.user.username+offset+'/'
        return render_to_response('OnlineTest.html',{'QuestionList':QuestionIdList,'URL':URL,'pagename':'Online Test'},context_instance=RequestContext(request))
#compute socre of student
def ReturnScore(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method =='POST':
        form = request.POST
        paperId = offset[-20:]
        student = request.user.username
        Student = Score.objects.get(StudentId=student,PaperId = paperId)
        PaperObject = Paper.objects.get(PaperId = paperId)
        paper = PaperObject.QId
        full = PaperObject.Full
        score = 0
        for i in range(20):
            QuestionL = Question.objects.get(QuestionId=paper[i*20:i*20+20])
            Answer = QuestionL.Answer
            SumScore = QuestionL.Score
            Id= '%s' % i
            answer = form.getlist(QuestionL.QuestionId)
            answer = str(''.join(answer))
            try:
                his = History.objects.get(PaperId = paperId,QuestionId = QuestionL.QuestionId)
            except History.DoesNotExist:
                his = History.objects.create(
                        PaperId = paperId,
                        QuestionId = QuestionL.QuestionId,
                        QIdError = 0,
                    )
            if not cmp(answer,Answer):
                score = score+SumScore
            else:
                his.QIdError = his.QIdError +1
                his.save()
        score = ceil(score/full*100)
        if Student.ValidScore < score:
            PaperObject.SumScore = PaperObject.SumScore +(score-Student.ValidScore)
            Student.ValidScore=score
            if score > PaperObject.MaxScore:
                PaperObject.MaxScore = score
            if score<PaperObject.MinScore:
                PaperObject.MinScore = score
        if Student.SubmitTimes is 0:
            PaperObject.SubmitNum = PaperObject.SubmitNum+1
        Student.SubmitTimes = Student.SubmitTimes+1
        Student.save()
        PaperObject.save()
        page = 'You\'ve got %d !<br><a href="/student/ViewPaper/">Return to View</a>'% (score)
        return HttpResponse(page)