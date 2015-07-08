
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

from django.contrib.auth.models import *
from django.contrib.auth import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout  
from  datetime  import  *  
import time
from classChoose.models import * 

#@csrf_protect  
#def alogin(request):
#	return render_to_response("login.html",context_instance=RequestContext(request))
@csrf_protect 
def alogin(request):  

	Count=count.objects.get(id="1")
	if Count.value>=200:
		return render_to_response("人太多了！")
	else:  
		a = "haha"
		print(a)
		errors= []  
		account=None  
		password=None  
		if request.method == 'POST' :  
			if not request.POST.get('username'):  
				errors.append('Please Enter account')  
			else:  
				account = request.POST.get('username')  
			if not request.POST.get('password'):  
				errors.append('Please Enter password')  
			else:  
				password= request.POST.get('password')  
			if account is not None and password is not None :  
				user = authenticate(username=account,password=password)  
				print("check")
				if user is not None:  
					if user.is_active:  
						login(request,user) 
						Count.value=Count.value+1
						Count.save()

						request.session.set_expiry(3600)
						print("checkOK")
						print(request.user.username)
						dir = '/daohang/?id=' + account;
						print(dir)

						return HttpResponseRedirect(dir)  
					else:  
						errors.append('disabled account')  
				else :  
					errors.append('invaild user')  
		return render_to_response('login.html',{"error":errors},context_instance=RequestContext(request))  

 
@login_required(login_url="/login/")  
def daohang(request):
	print(request.user.username)
	return render_to_response("daohang.html",context_instance=RequestContext(request))


@login_required(login_url="/login/")  
def logout(request):  
	Count=count.objects.get(id="1")
	Count.value=Count.value-1
	Count.save()

	user_logout(request)  

	print("logout")
	return HttpResponseRedirect("/login/") 


def forcelogout(request):
	Count=count.objects.get(id="1")
	Count.value=Count.value-1
	Count.save()

	timeminus =time.mktime(datetime.now().timetuple()) - time.mktime(request.user.last_login.timetuple())-28800
	if(timeminus>3600):
		user_logout(request) 
		return HttpResponseRedirect("/login/") 