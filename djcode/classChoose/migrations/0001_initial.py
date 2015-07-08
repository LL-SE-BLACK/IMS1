# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_users',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='buXuan_info',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('reason', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='choose_time',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
                ('buXuan_start_time', models.CharField(max_length=50)),
                ('buXuan_end_time', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Class_table',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('status', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Class_info',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('time', models.CharField(max_length=20)),
                ('room', models.CharField(max_length=20)),
                ('examdate', models.CharField(max_length=10)),
                ('examtime', models.CharField(max_length=10)),
                ('examroom', models.CharField(max_length=20)),
                ('capacity', models.IntegerField(default=0)),
                ('remain', models.IntegerField(default=0)),
                ('semester', models.IntegerField(default=0)),
                ('year', models.CharField(max_length=9)),
                ('method', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='college_demand',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('college', models.CharField(max_length=50)),
                ('majorCourse_demand', models.IntegerField(default=0)),
                ('optionCourse_demand', models.IntegerField(default=0)),
                ('generalCourse_demand', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course_info',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('college', models.CharField(max_length=50)),
                ('credits', models.FloatField(default=0)),
                ('semester', models.IntegerField(default=0)),
                ('textbook', models.CharField(max_length=110)),
                ('style', models.IntegerField(default=0)),
                ('introduce', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_users',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('introduce', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='pingjia',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('dengji', models.CharField(max_length=10)),
                ('Class', models.ForeignKey(to='classChoose.Class_info')),
            ],
        ),
        migrations.CreateModel(
            name='scheme_info',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=50)),
                ('state', models.IntegerField(default=0)),
                ('course', models.ForeignKey(related_name='scheme_course', to='classChoose.Course_info')),
            ],
        ),
        migrations.CreateModel(
            name='Student_user',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('gender', models.BooleanField(default=0)),
                ('college', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
                ('grade', models.IntegerField(default=0)),
                ('gpa', models.FloatField(default=0)),
                ('credits', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('password', models.CharField(max_length=20)),
                ('auth', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='scheme_info',
            name='student',
            field=models.ForeignKey(to='classChoose.Student_user'),
        ),
        migrations.AddField(
            model_name='pingjia',
            name='student',
            field=models.ForeignKey(to='classChoose.Student_user'),
        ),
        migrations.AddField(
            model_name='Class_info',
            name='course',
            field=models.ForeignKey(related_name='class_course', to='classChoose.Course_info'),
        ),
        migrations.AddField(
            model_name='Class_info',
            name='teacher',
            field=models.ForeignKey(to='classChoose.Faculty_users'),
        ),
        migrations.AddField(
            model_name='Class_table',
            name='Class',
            field=models.ForeignKey(to='classChoose.Class_info'),
        ),
        migrations.AddField(
            model_name='Class_table',
            name='student',
            field=models.ForeignKey(to='classChoose.Student_user'),
        ),
        migrations.AddField(
            model_name='buxuan_info',
            name='Class',
            field=models.ForeignKey(to='classChoose.Class_info'),
        ),
        migrations.AddField(
            model_name='buxuan_info',
            name='student',
            field=models.ForeignKey(to='classChoose.Student_user'),
        ),
    ]
