# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class_info',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('courseid', models.CharField(max_length=8)),
                ('teacher', models.CharField(max_length=20)),
                ('room', models.CharField(max_length=20)),
                ('examroom', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course_info',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=8)),
                ('name', models.CharField(max_length=110)),
                ('textbook', models.CharField(max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_user',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=6)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pre_requisites',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('courseid', models.CharField(max_length=8)),
                ('prereq', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Student_user',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
            ],
        ),
    ]
