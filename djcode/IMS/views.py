from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect
from django.core.files import File
import re
import os
from django.template.context import RequestContext

# Create your views here.
#def hello(request):
#        myfile = File(open(str(os.path.dirname(__file__))+'/static/data/log.txt','w'))
#        myfile.write(str(request.POST['changedRegion']))
#        return HttpResponse(request.POST)

def hello(request):
        return render(request,
                      'index.html')
