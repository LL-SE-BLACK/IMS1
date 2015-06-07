from django.shortcuts import *
from django.http import *



def home(request):
    return HttpResponse('hello')