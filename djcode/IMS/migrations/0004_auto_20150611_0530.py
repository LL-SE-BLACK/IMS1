# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0003_auto_20150609_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_user',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=3)),
                ('contact', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=20)),
                ('college', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='student_user',
            name='college',
            field=models.CharField(default='计算机科学与技术学院', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='contact',
            field=models.CharField(default='18812345678', max_length=11),
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
