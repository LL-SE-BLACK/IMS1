from django.contrib import admin

# Register your models here.
from IMS.models import *

admin.site.register(Student_user)
admin.site.register(Faculty_user)
admin.site.register(Admin_user)
admin.site.register(Course_info)
admin.site.register(Class_info)
admin.site.register(Pre_requisites)
admin.site.register(class_table)