# -*- coding: utf-8 -*-
__author__ = 'Adward'

from IMS.head import *
from IMS.models import Student_user, Faculty_user, Admin_user, FindPass
from IMS.profile_forms import StudentInfoForm
from django.http import Http404
from django import forms
from django.forms.util import ErrorList
from django.core.mail import EmailMessage
from djcode.settings import EMAIL_HOST_USER
from threading import Thread
import time
from djcode.settings import DOMAIN_NAME

class ForgetPwdForm(forms.Form):
    username = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(ForgetPwdForm, self).clean()
        _username = cleaned_data.get('username', '')
        if not User.objects.filter(username=_username):
            error_msg = ["用户不存在！"]
            super(ForgetPwdForm, self).errors['username'] = ErrorList(error_msg)
        else:
            pass
        return cleaned_data

def forget_pwd(request):
    form = ForgetPwdForm()
    t = get_template('forget_pwd.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))

def send_html_mail(subject, html_content, recipient_list):
    msg = EmailMessage(subject,
            html_content,
            EMAIL_HOST_USER,
            recipient_list)
    msg.content_subtype = "html"
    msg.send()

def random_string(request):
    pwd = ''
    seed = string.letters + string.digits
    for i in xrange(20):
        pwd += seed[random.randrange(1, len(seed))]
    return pwd

@csrf_exempt
def reset_pwd_mail(request):
    if request.method == 'POST':
        form = ForgetPwdForm(request.POST)
    else:
        form = ForgetPwdForm()

    if form.is_valid():
        _username = form.cleaned_data['username']
        user = User.objects.get(username=_username)
        addr = user.email
        #generate a random string with length [10,20]
        activation_key = random_string(random.randint(10, 20))
        #update username, key and timestamp into FindPass table
        #Detect the existence of the same user's previous unhandled request
        findPasses = FindPass.objects.filter(username=user.username)
        if findPasses: #exists a previous request
            findPass = findPasses[0]
            findPass.activation_key = activation_key #更新key
        else:
            findPass = FindPass(username=user.username,
                                activation_key=activation_key,
                                timestamp=int(time.time()))
        findPass.save()
        #send email
        t = get_template('reset_pwd_mail_content.html')
        c = RequestContext(request, {'username': _username,
                                     'url': 'http://'+DOMAIN_NAME+'/ims/reset_pwd/'+activation_key+'/'})
        #th = Thread(target=send_html_mail,
        #            args=('Password Reset from http://jwbinfosys.zju.edu.cn',
        #                'click the url http://127.0.0.1:8000/ims/reset_pwd/'+activation_key+'/',
        #                [addr])
        #            )
        th = Thread(target=send_html_mail,
                    args=('教务管理系统密码重设',
                          t.render(c),
                          [addr])
                    )
        th.start()
        return HttpResponseRedirect('/')

    # else, back to login page
    t = get_template('forget_pwd.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))

def reset_pwd(request, key):
    findPasses = FindPass.objects.filter(activation_key=key)
    if findPasses:
        findPass = findPasses[0]
        #Time is within 10 min
        if int(time.time())-int(findPass.timestamp) < 300 * 600:
            #reset passwd to default
            user = User.objects.get(username=findPass.username)
            user.set_password('123456')
            user.save()
            return render_to_response('pwd_reset_done.html')
    return HttpResponse("Out of time!")