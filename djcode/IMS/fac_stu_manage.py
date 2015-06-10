__author__ = 'John'

from IMS.head import *

from IMS.models import Student_user

def manage(request):
    return render(request, 'change_student&faculty.html')

def updateuser(request):
    print('jump')
    return render(request, 'updateuser.html')
