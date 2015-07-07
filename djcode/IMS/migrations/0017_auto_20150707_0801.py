# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0016_auto_20150702_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='FindPass',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=20)),
                ('activation_key', models.CharField(max_length=20)),
                ('timestamp', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='name',
            field=models.CharField(default='张三', max_length=20),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='college',
            field=models.CharField(default='计算机科学与技术学院', max_length=50),
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
    ]
