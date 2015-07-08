# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PaperId', models.CharField(max_length=20)),
                ('StudentId', models.CharField(max_length=20)),
                ('QIdError', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OnAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('OnAuthClassId', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PaperId', models.CharField(max_length=20)),
                ('PaperName', models.CharField(max_length=30)),
                ('QId', models.CharField(max_length=400)),
                ('Creator', models.CharField(max_length=20)),
                ('ClassId', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('QuestionId', models.CharField(max_length=20)),
                ('Stem', models.CharField(max_length=2000)),
                ('OptionA', models.CharField(max_length=100)),
                ('OptionB', models.CharField(max_length=100)),
                ('OptionC', models.CharField(max_length=100, blank=True)),
                ('OptionD', models.CharField(max_length=100, blank=True)),
                ('Answer', models.CharField(max_length=20)),
                ('Chapter', models.CharField(max_length=20)),
                ('Course', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('StudentId', models.CharField(max_length=20)),
                ('PaperId', models.CharField(max_length=20)),
                ('ValidScore', models.FloatField(null=True)),
                ('SubmitTimes', models.IntegerField(null=True)),
            ],
        ),
    ]
