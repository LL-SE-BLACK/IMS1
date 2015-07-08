# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0012_auto_20150701_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_user',
            name='name',
            field=models.CharField(default=b'\xe5\xbc\xa0\xe4\xb8\x89', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='college',
            field=models.CharField(default=b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe5\xad\xa6\xe9\x99\xa2', max_length=50),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='degree',
            field=models.CharField(default=b'\xe5\x8d\x9a\xe5\xa3\xab', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='major',
            field=models.CharField(default=b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf', max_length=50),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='name',
            field=models.CharField(default=b'\xe5\xbc\xa0\xe4\xb8\x89', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='title',
            field=models.CharField(default=b'\xe7\xa0\x94\xe7\xa9\xb6\xe5\x91\x98', max_length=20),
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
