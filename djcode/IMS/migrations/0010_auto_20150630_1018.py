# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import IMS.models


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0009_auto_20150624_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course_info',
            old_name='type',
            new_name='course_type',
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='college',
            field=models.CharField(default='all', max_length=50),
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='contact',
            field=models.CharField(default='18812345678', max_length=11),
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='name',
            field=models.CharField(default='张三', max_length=20),
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='photo',
            field=models.FileField(default='photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='college',
            field=models.CharField(default='计算机科学与技术学院', max_length=50),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='contact',
            field=models.CharField(default='18812345678', max_length=11),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='degree',
            field=models.CharField(default='博士', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='major',
            field=models.CharField(default='计算机科学与技术', max_length=50),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='name',
            field=models.CharField(default='张三', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='photo',
            field=models.FileField(default='photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='title',
            field=models.CharField(default='研究员', max_length=20),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='college',
            field=models.CharField(default='计算机科学与技术学院', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='major',
            field=models.CharField(default='计算机科学与技术', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='name',
            field=models.CharField(default='张三', max_length=20),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='photo',
            field=models.FileField(default='photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
        migrations.AlterField(
            model_name='sys_log',
            name='optype',
            field=models.CharField(default='update', max_length=20),
        ),
        migrations.AlterField(
            model_name='sys_log',
            name='post',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='sys_log',
            name='pre',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
