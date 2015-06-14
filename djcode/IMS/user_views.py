__author__ = 'John'

from IMS.head import *
from IMS.user_forms import FacultyForm, FacultyFormModify, StudentForm, StudentFormModify
from IMS.models import Faculty_user, Student_user

LEN_OF_FACULTY_TABLE = 8
LEN_OF_STUDENT_TABLE = 9

def userMain(request):
    return render(request, 'UserMain.html')

def facultyAdd(request):
    if request.user.is_anonymous():
        return render(request, 'UserMain.html')
    else:
        errors = []
        existed = []
        addIsDone = False
        if request.method == 'POST':
            if 'file' in request.POST and len(request.POST.get('file')) > 0:  # click confirm button
                fileTerms = re.split(',', request.POST.get('file'))
                s = ""
                for x in range(0, len(fileTerms) / LEN_OF_FACULTY_TABLE):
                    dbQuery = Faculty_user(
                        id = fileTerms[0 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        contact = fileTerms[1 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        name = fileTerms[2 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        gender = fileTerms[3 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        college = fileTerms[4 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        major = fileTerms[5 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        degree = fileTerms[6 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                        title = fileTerms[7 + LEN_OF_FACULTY_TABLE * x].encode('utf-8'),
                    )
                    if Faculty_user.objects.filter(id = fileTerms[0 + LEN_OF_FACULTY_TABLE * x]):  #test duplicate add
                        s = s + str(x)
                        isExist = True
                        existed.append(
                            fileTerms[0 + x * LEN_OF_FACULTY_TABLE: LEN_OF_FACULTY_TABLE + x * LEN_OF_FACULTY_TABLE])
                    else:
                        dbQuery.save()
                addIsDone = True
                form = FacultyForm()
            elif request.FILES.get('file'):  # dealing with upload
                fileLocation = request.FILES.get('file')
                fileTerms = re.split(',|\n', fileLocation.read())
                multiAdd = True
                terms = []
                for x in range(0, len(fileTerms) / LEN_OF_FACULTY_TABLE):
                    terms.append(
                        fileTerms[0 + x * LEN_OF_FACULTY_TABLE: LEN_OF_FACULTY_TABLE + x * LEN_OF_FACULTY_TABLE])
            elif request.POST.get('multiAddCancle'):  # click cancle button
                form = FacultyForm()
            else:  # regular form submit
                form = FacultyForm(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Faculty_user(
                        id = info['id'],
                        contact = info['contact'],
                        name = info['name'],
                        gender = info['gender'],
                        college = info['college'],
                        major = info['major'],
                        degree = info['degree'],
                        title = info['title']
                    )
                    dbQuery.save()
                    addIsDone = True
                    form = FacultyForm()
        else:  # raw form
            form = FacultyForm()
        return render(request, 'AddFaculty.html', locals())

def facultyDelete(request):
    errors = []
    response = render(request, 'DeleteFaculty.html', locals())
    if request.method == 'GET':
        if 'term' in request.GET:
            inSearch = True
            searchTerm = request.GET.get('term')
            searchType = request.GET.get('type')
            if not searchTerm:
                errors.append('Please enter a key word')
                response = render(request, 'DeleteFaculty.html', locals())
            else:
                if searchType  ==   'id':
                    faculties = Faculty_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    faculties = Faculty_user.objects.filter(name__icontains = searchTerm)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
                response = render(request, 'DeleteFaculty.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
    elif request.method  ==   'POST':
        if 'deleteid' in request.POST:
            facultyId = request.POST.get('deleteid')
            Faculty_user.objects.filter(id = facultyId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType  ==   'id':
                    faculties = Faculty_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    faculties = Faculty_user.objects.filter(name__icontains = searchTerm)
            response = render(request, 'DeleteFaculty.html', locals())
    return response

def facultyModify(request):
    errors = []
    if request.method  ==   'GET':
        if 'term' in request.GET:
            inSearch = True
            searchTerm = request.GET.get('term')
            searchType = request.GET.get('type')
            if not searchTerm:
                errors.append('Please enter a key word')
            else:
                if searchType  ==   'id':
                    faculties = Faculty_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    faculties = Faculty_user.objects.filter(name__icontains = searchTerm)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
    if request.method  ==   'POST':
        if 'modifyid' in request.POST:
            inModify = True
            facultyId = request.POST.get('modifyid')
            term = Faculty_user.objects.filter(id = facultyId)
            form = FacultyFormModify(initial = {
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college,
                'major': term[0].major,
                'degree': term[0].degree,
                'title': term[0].title}
                                     )
        else:
            form = FacultyFormModify(request.POST)
            if form.is_valid():
                info = form.cleaned_data
                dbQuery = Faculty_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college'],
                    major = info['major'],
                    degree = info['degree'],
                    title = info['title']
                )
                dbQuery.save()
                modifyIsDone = True
    return render(request, 'ModifyFaculty.html', locals())


def studentAdd(request):
    if request.user.is_anonymous():
        return render(request, 'UserMain.html')
    else:
        errors = []
        existed = []
        addIsDone = False
        if request.method  ==   'POST':
            if 'file' in request.POST and len(request.POST.get('file')) > 0:  # click confirm button
                fileTerms = re.split(',', request.POST.get('file'))
                s = ""
                for x in range(0, len(fileTerms) / LEN_OF_STUDENT_TABLE):
                    dbQuery = Student_user(
                        id = fileTerms[0 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        contact = fileTerms[1 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        name = fileTerms[2 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        gender = fileTerms[3 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        college = fileTerms[4 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        major = fileTerms[5 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        grade = fileTerms[6 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        gpa = fileTerms[7 + LEN_OF_STUDENT_TABLE * x].encode('utf-8'),
                        credits = fileTerms[8 + LEN_OF_STUDENT_TABLE * x].encode('utf-8')
                    )
                    if Student_user.objects.filter(id = fileTerms[0 + LEN_OF_STUDENT_TABLE * x]):  #test duplicate add
                        s = s + str(x)
                        isExist = True
                        existed.append(
                            fileTerms[0 + x * LEN_OF_STUDENT_TABLE: LEN_OF_STUDENT_TABLE + x * LEN_OF_STUDENT_TABLE])
                    else:
                        dbQuery.save()
                addIsDone = True
                form = StudentForm()
            elif request.FILES.get('file'):  # dealing with upload
                fileLocation = request.FILES.get('file')
                fileTerms = re.split(',|\n', fileLocation.read())
                multiAdd = True
                terms = []
                for x in range(0, len(fileTerms) / LEN_OF_STUDENT_TABLE):
                    terms.append(
                        fileTerms[0 + x * LEN_OF_STUDENT_TABLE: LEN_OF_STUDENT_TABLE + x * LEN_OF_STUDENT_TABLE])
            elif request.POST.get('multiAddCancle'):  # click cancle button
                form = StudentForm()
            else:  # regular form submit
                form = StudentForm(request.POST)
                if form.is_valid():
                    info = form.cleaned_data
                    dbQuery = Student_user(
                        id = info['id'],
                        contact = info['contact'],
                        name = info['name'],
                        gender = info['gender'],
                        college = info['college'],
                        major = info['major'],
                        grade = info['grade'],
                        gpa = info['gpa'],
                        credits = info['credits']
                    )
                    dbQuery.save()
                    addIsDone = True
                    form = StudentForm()
        else:  # raw form
            form = StudentForm()
        return render(request, 'AddStudent.html', locals())

def studentDelete(request):
    errors = []
    response = render(request, 'DeleteStudent.html', locals())
    if request.method  ==   'GET':
        if 'term' in request.GET:
            inSearch = True
            searchTerm = request.GET.get('term')
            searchType = request.GET.get('type')
            if not searchTerm:
                errors.append('Please enter a key word')
                response = render(request, 'DeleteStudent.html', locals())
            else:
                if searchType  ==   'id':
                    students = Student_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    students = Student_user.objects.filter(name__icontains = searchTerm)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
                response = render(request, 'DeleteStudent.html', locals())
                response.set_cookie('deleteTerm', searchTerm)
                response.set_cookie('deleteType', searchType)
    elif request.method  ==   'POST':
        if 'deleteid' in request.POST:
            studentId = request.POST.get('deleteid')
            Student_user.objects.filter(id = studentId).delete()
            isDeleted = True
            if 'deleteTerm' in request.COOKIES and 'deleteType' in request.COOKIES:
                searchTerm = request.COOKIES['deleteTerm']
                searchType = request.COOKIES['deleteType']
                if searchType  ==   'id':
                    students = Student_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    students = Student_user.objects.filter(name__icontains = searchTerm)
            response = render(request, 'DeleteStudent.html', locals())
    return response

def studentModify(request):
    errors = []
    if request.method  ==   'GET':
        if 'term' in request.GET:
            inSearch = True
            searchTerm = request.GET.get('term')
            searchType = request.GET.get('type')
            if not searchTerm:
                errors.append('Please enter a key word')
            else:
                if searchType  ==   'id':
                    students = Student_user.objects.filter(id = searchTerm)
                elif searchType  ==   'name':
                    students = Student_user.objects.filter(name__icontains = searchTerm)
                # else:
                #courses = Course_info.objects.filter(teacher = searchTerm)
    if request.method  ==   'POST':
        if 'modifyid' in request.POST:
            inModify = True
            studentId = request.POST.get('modifyid')
            term = Student_user.objects.filter(id = studentId)
            form = StudentFormModify(initial = {
                'contact': term[0].contact,
                'name': term[0].name,
                'gender': term[0].gender,
                'college': term[0].college,
                'major': term[0].major,
                'grade': term[0].grade,
                'gpa': term[0].gpa,
                'credits' : term[0].credits}
                                     )
        else:
            form = StudentFormModify(request.POST)
            if form.is_valid():
                info = form.cleaned_data
                dbQuery = Student_user(
                    id = info['id'],
                    contact = info['contact'],
                    name = info['name'],
                    gender = info['gender'],
                    college = info['college'],
                    major = info['major'],
                    grade = info['grade'],
                    gpa = info['gpa'],
                    credits = info['credits']
                )
                dbQuery.save()
                modifyIsDone = True
    return render(request, 'ModifyStudent.html', locals())
