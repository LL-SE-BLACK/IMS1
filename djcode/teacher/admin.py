from django.contrib import admin
from teacher.models import *
# Register your models here.
admin.site.register(Question)
admin.site.register(Paper)
admin.site.register(Score)
admin.site.register(History)
admin.site.register(MyAuth)