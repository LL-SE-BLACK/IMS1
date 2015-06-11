# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0004_auto_20150611_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_user',
            name='gender',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='examtime',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course_info',
            name='credits',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='course_info',
            name='semester',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='faculty_user',
            name='gender',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='college',
            field=models.CharField(default=b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe5\xad\xa6\xe9\x99\xa2', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='major',
            field=models.CharField(default=b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='name',
            field=models.CharField(default=b'\xe5\xbc\xa0\xe4\xb8\x89', max_length=20),
        ),
    ]
