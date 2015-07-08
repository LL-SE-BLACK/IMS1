# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0015_auto_20150701_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='Admin_user',
            options={'permissions': (('admin_manage', 'Can manage admin user info'),)},
        ),
        migrations.AlterModelOptions(
            name='Course_info',
            options={'permissions': (('course_manage', 'Can manage basic course info'),)},
        ),
        migrations.AlterModelOptions(
            name='Faculty_user',
            options={'permissions': (('faculty_manage', 'Can manage faculty user info'),)},
        ),
        migrations.AlterModelOptions(
            name='student_user',
            options={'permissions': (('student_manage', 'Can manage stu user info'),)},
        ),
    ]
