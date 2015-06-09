# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0002_auto_20150605_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_user',
            name='credits',
            field=models.FloatField(default=100.0),
        ),
        migrations.AddField(
            model_name='student_user',
            name='gender',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student_user',
            name='gpa',
            field=models.FloatField(default=4.0),
        ),
        migrations.AddField(
            model_name='student_user',
            name='grade',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='college',
            field=models.CharField(default=b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf\xe5\xad\xa6\xe9\x99\xa2', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='contact',
            field=models.CharField(default=b'18812345678', max_length=11),
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
