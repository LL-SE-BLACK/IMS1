# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from form import PaperGenerateForm,CHQuestionAddForm,JUQuestionAddForm,QuestionSearchForm
from django.http import Http404,HttpResponseRedirect,HttpResponse
from math import exp
import random
from student.views import getquestion
from models import Paper, Question, Score, History,MyAuth
from IMS.models import Class_info,Student_user,Course_info,Faculty_user
import datetime
import re
import os
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission
from decimal import *
#from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Create your views here.
# select question by given chapter and the total number of Difficulty

def get_class(request):
    UserID = request.user.username
    UserClass = MyAuth.objects.get(UserId=UserID)
    return UserClass

def SelectQuestion(ChL,ChH,Type_i,Num,Diff,request):  # used to select question from question BANK
    SelectQue = []
    mysum = 0
    p =[]
    for i in [1,2,3,4,5]:
        p.append(exp(-abs(i-Diff)))
    sum_p = sum(p)
    for i in [2,3,4,5]:
        p[i-1] = p[i-1]/sum_p
        NumQ = int(round(Num*p[i-1]))
        mysum +=NumQ

        UserClassId = get_class(request).OnAuthClassId
        courseInfo = Class_info.objects.get(class_id=UserClassId).course_id
        courseId = courseInfo.course_id
        Q = Question.objects.filter(Chapter__in=range(ChL,ChH+1), Type__in=Type_i, Difficulty=i,CourseId=courseId)
        #SelectQue
        if len(Q)<NumQ:
            return []
        else:
            for i in random.sample(range(len(Q)),NumQ):
                SelectQue.append(Q[i])
    Q = Question.objects.filter(Chapter__in=range(ChL,ChH+1), Type__in=Type_i, Difficulty=1)
    NumQ = Num-mysum
    if len(Q)<NumQ:
        return []
    else:
        for i in random.sample(range(len(Q)),NumQ):
            SelectQue.append(Q[i])
    return SelectQue
#After generate paper, adjust some of questions.
def PaperAdjust(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.POST:
        QuestionNum = 0
        try:
            paper = Paper.objects.get(PaperId = offset)
        except Paper.DoesNotExist:
            raise Http404
        form = request.POST
        Question = form.getlist('list')
        if not Question:
            return HttpResponseRedirect('/teacher/AutoGenerate/')
        qid = [int(id) for id in Question] # the id of all the deleted question
        Qid = paper.QId #old version of qid in paper
        q = '' # update question id
        for id in range(20):
            if id not in qid:
                q = q+ Qid[id*20:id*20+20]  # add to the tail of q if not to be deleted
            else:
                QuestionNum += 1
        paper.QId = q
        paper.save()
        QuestionList = []
        PaperId = paper.PaperId
        pagename='Paper Manual Generate'
        return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
#This view is used to generate paper automatically
def PaperAutoGenerate(request):
    # here we need user_auth
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    errors = []
    if request.POST:
        cd = request.POST
        chL= cd['ChL']
        chH = cd['ChH']
        SNum = cd['SelectNum']
        JNum = cd['CheckNum']
        Diff = cd['Difficulty']
        Name = cd['PaperName']
        Start = cd['StartTime']
        start = re.sub(r'\.','-',Start)
        mtime2 = cd['mytime2']
        Dead =cd['DeadLine']
        dead = re.sub(r'\.','-',Dead)
        mtime = cd['mytime']
        if mtime is u'':
            deadline = None
        else:
            deadline = dead+' '+mtime
        if mtime2 is u'':
            starttime = None
        else:
            starttime = start+' '+mtime2
        try:
            Diff = int(Diff)
            SNum = int(SNum)
            JNum = int(JNum)
            chL = int(chL)
            chH = int(chH)
        except ValueError:
            errors.append('Please input integer!')
            return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
        if chL > chH:
            errors.append('Low Chapter is higher than Upper!')
            return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
        ChL = SelectQuestion(chL,chH, [2,3], SNum, Diff,request)
        if not ChL:
            errors.append('Not Enough Select Question!')
            return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
        JuL = SelectQuestion(chL, chH,[1], JNum, Diff,request)
        if not JuL:
            errors.append('Not Enough Judge Question')
            return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
        QuestList = [ChL, JuL]
        # add paper into database
        Qid = ''
        mylist = []
        full = 0
        for questionL in QuestList:
            for question in questionL:
                Qid = Qid + question.QuestionId
                full = full+question.Score
                mylist.append(question)
        paperid = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        paperid = request.user.username + paperid[-(20-len(request.user.username)):]
        classId = get_class(request).OnAuthClassId
        paper = Paper.objects.create(PaperId= paperid,
                            PaperName = Name,
                            QId = Qid,
                            Creator = request.user.username,
                            # jfaj
                            MaxScore = 0,
                            MinScore = 10000,
                            SumScore = 0,
                            SubmitNum = 0,
                            Full=full,
                            ClassId = classId,
                            StartTime = starttime,
                            #Deadline = Dead )
                             Deadline = deadline)
        #return HttpResponse('create paper successfully!')
        return render_to_response('P_view_tea.html', {'QuestionList': mylist,'Paper':paper,'Full':full},context_instance=RequestContext(request))
    return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
#After generate paper, teacher choose cancel
def PaperD(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/');
    if request.POST:
        errors = []
        try:
            paper = Paper.objects.get(PaperId = offset)
        except Paper.DoesNotExist:
            raise Http404
        paper.delete()
        # return render_to_response('P_auto.html', {'errors': errors},context_instance=RequestContext(request))
        return HttpResponseRedirect('/teacher/AutoGenerate/')
# generate paper manually---search with given condition
def PaperManualGenerate(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    QuestionList = []
    PaperId = offset
    if len(offset) == 20:
        QIDlength = len(Paper.objects.get(PaperId=offset).QId)
        QuestionNum = (400 - QIDlength) / 20
    else:
        QuestionNum = 20
    pagename='Paper Manual Generate'
    if request.POST:
        form = request.POST
        chL = form['ChapterL']
        chU = form['ChapterU']
        if chL is u'':
            chL = 1
        if chU is u'':
            chU = 100
        dfl = form['DifL']
        dfu = form['DifU']
        if dfl is u'':
            dfl = 1
        if dfu is u'':
            dfu = 5
        keyword = form['Keyword']
        type_i = form['Type']
        try:
            type_i = int(type_i)
            dfl = int(dfl)
            dfu = int(dfu)
            chL = int(chL)
            chU = int(chU)
        except ValueError:
            return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
        if (dfl>dfu) or (chU<chL) or (dfl<=0) or (dfu>6) or chL<=0 or chU>100:
            return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
        if type_i is 0:
            type_i = [1,2,3]
        else:
            type_i = [type_i]
        if keyword is '':
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Difficulty__in=range(dfl,dfu+1),Flag=1)
        else:
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Stem__icontains=keyword,Difficulty__in=range(dfl,dfu+1),Flag=1)
    return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
#Generate paper manually--generate paper according to user's selection
def PaperMaG(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.POST:
        errors = ''
        form = request.POST
        creator = request.user.username
        Qid = form.getlist('Option')
        try:
           PaperL = Paper.objects.get(PaperId=offset)
           QID =PaperL.QId
           num = 20-len(QID)/20
           QuestionNum = num
           if len(Qid) is not num:
                return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
           full = 0
           qid = ''  #generate as select
           for q in   Qid:
               que = Question.objects.get(QuestionId=q)
               full = full+que.Score
               qid = qid + q
           PaperL.QId = PaperL.QId + qid
           PaperL.Full = PaperL.Full+full
           PaperL.save()
           mylist = getquestion(PaperL.QId)
           paper = PaperL
           return render_to_response('P_view_tea.html', {'QuestionList': mylist,'Paper':paper,'Full':full},context_instance=RequestContext(request))
        except Paper.DoesNotExist:
            Dead =form['DeadLine']
            Start = form['StartTime']
            start = re.sub(r'\.','-',Start)
            mtime2 = form['mytime2']
            dead = re.sub(r'\.','-',Dead)
            mtime = form['mytime']
            if mtime is u'':
                deadline = None
            else:
                deadline = dead+' '+mtime
            if mtime2 is u'':
                starttime = None
            else:
                starttime = start+' '+mtime2
            papername = form['PaperName']
            paperid = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
            paperid = creator + paperid[-(20-len(request.user.username)):]
            QuestionNum = 20
            if len(Qid) is not 20:
                return render_to_response('P_manual.html',locals(),context_instance=RequestContext(request))
            full = 0
            qid = ''  #generate as select
            for q in   Qid:
                que = Question.objects.get(QuestionId=q)
                full = full+que.Score
                qid = qid + q
            classId = get_class(request).OnAuthClassId
            Paper.objects.create(
                    PaperId = paperid,
                    PaperName = papername,
                    QId = qid,
                    Creator =creator,
                    ClassId = classId,
                    StartTime = starttime,
                    Deadline = deadline,
                    MaxScore = 0,
                    MinScore =10000,
                    SumScore = 0,
                    SubmitNum = 0,
                    Full = full
                    )
    return HttpResponse('You\'ve sucessfully genreate a paper!<br><a href="/teacher/ManualGenerate/">Return to Manual generate page or do another</a>')
# generate a analysis with specific paper
def PaperA(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.POST:
        pagename = 'Paper Name'
        try:
           PaperL = Paper.objects.get(PaperId=offset)
        except Paper.DoesNotExist:
           raise Http404()
        # get different distribution of score
        ScoreList = Score.objects.filter(PaperId=offset)
        S = [0,0,0,0,0,0,0,0,0,0]
        S_name = ['(0,10]','(10,20]','(20,30]','(30,40]','(40,50]','(50,60]','(60,70]','(70,80]','(80,90]','(90,100]']
        for score in ScoreList:
            idx = int(round(score.ValidScore/10))
            S[idx] = S[idx]+1
        history=History.objects.filter(PaperId = offset)
        if not history:
            return  HttpResponse('No student has do this paper!<br><a href="/teacher/PaperAnalysis/">return</a>')
        ChError = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ChNum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        TypeE = [0,0,0]
        TypeNum = [0,0,0]
        TypeName = ['Single','Multi','Judge']
        for his in history:
            qid = his.QuestionId
            question = Question.objects.get(QuestionId=qid)
            ch = question.Chapter
            type = question.Type
            # 1 choose 3- judge 1. single 2 , mutli 3. judge
            TypeE[type-1] = TypeE[type-1]+his.QIdError
            TypeNum[type-1] = TypeNum[type-1]+1
            ChError[ch-1] = ChError[ch-1]+his.QIdError
            ChNum[ch-1] = ChNum[ch-1]+1
        typeError = [0.0,0.0,0.0];
        for i in range(3):
            if TypeNum[i] is not 0:
                typeError[i] =TypeE[i]*1.0/TypeNum[i]
            else:
                typeError[i] = 0.0
        Error = []
        ErrorName = []
        for i in range(len(ChNum)):
            if ChNum[i] is not 0:
                Error.append(ChError[i]*1.0/ChNum[i])
                name = 'Ch %d'%(i+1)
                ErrorName.append(name)
        return render_to_response('P_Analy_t.html',locals(),context_instance=RequestContext(request))
# show all of paper need to be analysed
def PaperAnalysis(request):
    #this view generate PapeAnalysis with ID (get from url)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.POST:
        # get score
        pagename = 'PaperAnalysis'
        teacher = request.user.username
        paper= Paper.objects.filter(Creator = teacher,ClassId='0000000001')
        PaperList =[]
        for paperItem in  paper:
            URL = '/teacher/Analysis/'+paperItem.PaperId+'/'
            PaperList.append({'PaperName':paperItem.PaperName,'URL':URL})
        return render_to_response('P_Analy.html',locals(),context_instance=RequestContext(request))
# search and show result
def QuestionModify(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user_auth/')
    QuestionList = []
    if request.method == 'POST':
        form = request.POST
        chL = form['ChapterL']
        chU = form['ChapterU']
        if chL is u'':
            chL = 1
        if chU is u'':
            chU = 100
        dfl = form['DifL']
        dfu = form['DifU']
        if dfl is u'':
            dfl = 1
        if dfu is u'':
            dfu = 5
        keyword = form['Keyword']
        type_i = form['Type']
        try:
            type_i = int(type_i)
            dfl = int(dfl)
            dfu = int(dfu)
            chL = int(chL)
            chU = int(chU)
        except ValueError:
            return render_to_response('Q_mod.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
        if (dfl>dfu) or (chU<chL) or (dfl<=0) or (dfu>6) or chL<=0 or chU>100:
            return render_to_response('Q_mod.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
        if type_i is 0:
            type_i = [1,2,3]
        else:
            type_i = [type_i]
        if keyword is '':
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Difficulty__in=range(dfl,dfu+1),Flag=1)
        else:
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Stem__icontains=keyword,Difficulty__in=range(dfl,dfu+1),Flag=1)
    return render_to_response('Q_mod.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
#modify question in database
def QuestionM(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user_auth/')
    if request.POST:
        QuestionName = Question.objects.filter(QuestionId=offset)
        if not QuestionName:
            return HttpResponse('<html>Question Do not Exist!</html>')
        form = request.POST;
        option = form.getlist('Option')
        option= str(''.join(option))
        if len(option)<=0:
            return HttpResponse('<html>No Answer!</html>')
        difficulty = form['Difficulty']
        score = form['Score']
        stem = form['Stem']
        try:
            difficulty = int(difficulty)
            score = int(score)
        except ValueError:
            return HttpResponse('<html>TYpe ERROR!</html>')
        try:
            optionA = form['OptionA']
            optionB = form['OptionB']
            optionC = form['OptionC']
            optionD = form['OptionD']
            if (optionA is u'') or (optionB is u'') or (optionC is u'') or (optionD is u''):
                return HttpResponse('You input no options!')
            QuestionName.update(Difficulty = difficulty,Stem=stem,Score=score,Answer = option,OptionA=optionA,OptionB=optionB,OptionC=optionC,OptionD=optionD)
        except KeyError:
            QuestionName.update(Difficulty = difficulty,Stem=stem,Score=score,Answer = option)
        page = 'Modify successfully!<br><a href="/teacher/ModifyQuestion/">Return to Modify or another</a>'
        return HttpResponse(page)
#delete selected question in database(actually not really delete, set flag=0)
def QuestionD(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.POST:
        x = '<a href = "/teacher/DeleteQuestion/">Return to Deltete</a>'
        try:
            QuestionName = Question.objects.filter(QuestionId = offset).update(Flag=0)
            page = 'Delete Sucessfully!<br>'+x
            return HttpResponse(page)
        except Question.DoesNotExist:
            page = 'Question Does Not Exist!<br>'+x
            return HttpResponse(page)
#search question and show result to delete
def QuestionDelete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    QuestionList = []
    if request.method == 'POST':
        form = request.POST
        chL = form['ChapterL']
        chU = form['ChapterU']
        if chL is u'':
            chL = 1
        if chU is u'':
            chU = 100
        dfl = form['DifL']
        dfu = form['DifU']
        if dfl is u'':
            dfl = 1
        if dfu is u'':
            dfu = 5
        keyword = form['Keyword']
        type_i = form['Type']
        try:
            type_i = int(type_i)
            dfl = int(dfl)
            dfu = int(dfu)
            chL = int(chL)
            chU = int(chU)
        except ValueError:
            return render_to_response('Q_del.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
        if (dfl>dfu) or (chU<chL) or (dfl<=0) or (dfu>6) or chL<=0 or chU>100:
            return render_to_response('Q_del.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
        if type_i is 0:
            type_i = [1,2,3]
        else:
            type_i = [type_i]
        if keyword is '':
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Difficulty__in=range(dfl,dfu+1),Flag=1)
        else:
            QuestionList = Question.objects.filter(Chapter__in=range(chL,chU+1),Type__in=type_i,Stem__icontains=keyword,Difficulty__in=range(dfl,dfu+1),Flag=1)
    return render_to_response('Q_del.html',{'pagename':'modify question','QuestionList':QuestionList},context_instance=RequestContext(request))
#show a page to add different kind of question
def QuestionAdd(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.POST:
        #return  HttpResponse('hello')
        return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
# add select question
def QuestionAddForm1(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.POST:
        form = request.POST
        sOptionA = form['SOptionA']
        sOptionB = form['SOptionB']
        sOptionC = form['SOptionC']
        sOptionD = form['SOptionD']
        if (sOptionC is '') or (sOptionB is '') or (sOptionA is '') or (sOptionD is ''):
            return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
        score = form['Score']
        difficulty = form['Difficulty']
        chapter = form['Chapter']
        stem = form['Stem']
        answer = str(''.join(request.POST.getlist('SOptionc')))
        try:
            difficulty = int(difficulty)
            chapter = int(chapter)
            score = int(score)
        except ValueError:
            return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
        if (difficulty<0)or (score<=0) or (difficulty>6) or (chapter<=0) or (chapter>100) or (stem is ''):#or (len(answer) is 0):
            return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
        flag = 1
        if answer>1:
            type_i = 3
        else:
            type_i = 2
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        length = len(str(request.user.username))
        questionId = request.user.username + questionId[0:(20-length)]
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                OptionA = sOptionA,
                                OptionB = sOptionB,
                                OptionC = sOptionC,
                                OptionD = sOptionD,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = get_class(request),
                                Score = score,
            )
        x = '<a href = "/teacher/AddQuestion/">Return to Add</a>'
        page =  'create successfully<br>'+x
        return HttpResponse(page)
#add judge question
def QuestionAddForm2(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.POST:
        #course = # you need to get the course_id of the curerent user
        form = request.POST
        score = form['Score']
        difficulty = form['Difficulty']
        chapter = form['Chapter']
        stem = form['JStem']
        answer = form['JTr']
        try:
            difficulty = int(difficulty)
            chapter = int(chapter)
            score = int(score)
        except ValueError:
            return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
        if (difficulty<0)or (score<=0) or (difficulty>6) or (chapter<=0)or(chapter>100) or (stem is ''):#or (len(answer) is 0):
            return render_to_response('Q_add.html',{'pagename':'Add Questions'},context_instance=RequestContext(request))
        flag = 1
        '''if answer>1:
            type_i = 3
        else:
            type_i = 2'''
        type_i = 1
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        length = len(str(request.user.username))
        questionId = request.user.username + questionId[0:(20-length)]
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
             #                   OptionA = sOptionA,
              #                  OptionB = sOptionB,
               #                 OptionC = sOptionC,
                #                OptionD = sOptionD,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = str(answer),
                                Chapter = chapter,
                                CourseId = get_class(request),
                                Score = score,
            )
        x = '<a href = "/teacher/AddQuestion/">Return to Add</a>'
        page =  'create successfully<br>'+x
        return HttpResponse(page)
#function used to generate a question list of a paper
def getpaper(PaperList):
    paper = []
    for papername in PaperList:
        PaperId = papername.PaperId
        now = datetime.datetime.now()
        start = papername.StartTime
        end = papername.Deadline
        IsStart = 1
        IsEnd = 1
        if start:
            start = start.replace(tzinfo=None)
            if start > now:
                IsStart = 0
            else:
                IsStart = 1
        else:
            IsStart = 0
        if end :
            end=end.replace(tzinfo=None)
            if end < now:
                IsEnd = 1
            else:
                IsEnd  =0
        else:
            IsEnd = 0
        PaperName = papername.PaperName
        paper.append({'PaperId':PaperId,'IsEnd':IsEnd,'IsStart':IsStart,'PaperName':PaperName})
    return paper
#used to set start time or deadline as now
def PaperManagement(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if not request.POST:
        # get score
        pagename = 'Paper Management'
        teacher = request.user.username
        PaperList= Paper.objects.filter(Creator = teacher,ClassId='0000000001')
        PaperList = getpaper(PaperList)
        return render_to_response('P_manage.html',locals(),context_instance=RequestContext(request))
        return render_to_response('P_manage.html',locals(),context_instance=RequestContext(request))
    else:
        IsStart = 0
        if not offset:
            return  HttpResponseRedirect('teacher/PaperManagement')
        a = int(offset[0])
        offset = offset[1:]
        if a is 0:
            IsStart = 1
        try:
            paper = Paper.objects.get(PaperId = offset)
        except Paper.DoesNotExist:
            raise Http404()
        now = datetime.datetime.now()
        if IsStart is 1:
            paper.StartTime = now
        else:
            paper.Deadline = now
        paper.save()
        teacher = request.user.username
        PaperList= Paper.objects.filter(Creator = teacher,ClassId='0000000001')
        PaperList = getpaper(PaperList)
        return render_to_response('P_manage.html',locals(),context_instance=RequestContext(request))

'''
def newf(request):
    for i  in range(20):
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        stem = questionId + 'hello,kitty'+questionId
        sOptionA = questionId + 'hello,kitty'+'A'
        sOptionB = questionId + 'hello,kitty'+'B'
        sOptionC = questionId + 'hello,kitty'+'C'
        sOptionD = questionId + 'hello,kitty'+'D'
        type_i = 3
        difficulty = i%5+1
        flag = 1
        answer = 'ACD'
        chapter = i%20+1
        score = i%10+1
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                OptionA = sOptionA,
                                OptionB = sOptionB,
                                OptionC = sOptionC,
                                OptionD = sOptionD,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = '00000001',
                                Score = score,
            )
    for i  in range(20):
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        stem = questionId + 'hello,kitty'+questionId
        sOptionA = questionId + 'hello,kitty'+'A'
        sOptionB = questionId + 'hello,kitty'+'B'
        sOptionC = questionId + 'hello,kitty'+'C'
        sOptionD = questionId + 'hello,kitty'+'D'
        type_i = 2
        difficulty = i%5+1
        flag = 1
        answer = 'A'
        chapter = i%20+1
        score = i%10+1
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                OptionA = sOptionA,
                                OptionB = sOptionB,
                                OptionC = sOptionC,
                                OptionD = sOptionD,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = '00000001',
                                Score = score,
            )
    for i  in range(20):
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        stem = questionId + 'hello,kitty'+questionId
        sOptionA = questionId + 'hello,kitty'+'A'
        sOptionB = questionId + 'hello,kitty'+'B'
        sOptionC = questionId + 'hello,kitty'+'C'
        sOptionD = questionId + 'hello,kitty'+'D'
        type_i = 2
        difficulty = i%5+1
        flag = 1
        answer = 'C'
        chapter = i%20+1
        score = i%10+1
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                OptionA = sOptionA,
                                OptionB = sOptionB,
                                OptionC = sOptionC,
                                OptionD = sOptionD,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = '00000001',
                                Score = score,
            )
    for i  in range(20):
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        stem = questionId + 'hello,kitty'+questionId
        type_i = 1
        difficulty = i%5+1
        flag = 1
        answer = 'F'
        chapter = i%20+1
        score = i%10+1
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = '00000001',
                                Score = score,
            )
    for i  in range(20):
        questionId = re.sub(r'[-:\\.\\ ]','',str(datetime.datetime.now()))
        stem = questionId + 'hello,kitty'+questionId
        type_i = 1
        difficulty = i%5+1
        flag = 1
        answer = 'T'
        chapter = i%20+1

        score = i%10+1
        Question.objects.create(QuestionId =questionId,
                                Stem = stem,
                                Type = type_i,
                                Difficulty = difficulty,
                                Flag = flag,
                                Answer = answer,
                                Chapter = chapter,
                                CourseId = '00000001',
                                Score = score,
            )
    return HttpResponse('why should i return ?')
'''