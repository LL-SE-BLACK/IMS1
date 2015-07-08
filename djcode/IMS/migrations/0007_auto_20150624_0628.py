# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0006_auto_20150612_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sys_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.CharField(max_length=20)),
                ('optype', models.CharField(default=b'update', max_length=20)),
                ('table', models.CharField(max_length=20)),
                ('primkey', models.CharField(max_length=20)),
                ('field', models.CharField(max_length=20)),
                ('pre', models.CharField(default=b'none', max_length=50)),
                ('post', models.CharField(default=b'none', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='admin_user',
            name='photo',
            field=models.FileField(default=b'default.jpg', upload_to=b'photo'),
        ),
        migrations.AddField(
            model_name='class_info',
            name='language',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='remain',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='semester',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class_info',
            name='year',
            field=models.IntegerField(default=2015),
        ),
        migrations.AddField(
            model_name='course_info',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='faculty_user',
            name='isSpecial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='faculty_user',
            name='photo',
            field=models.FileField(default=b'default.jpg', upload_to=b'photo'),
        ),
        migrations.AddField(
            model_name='student_user',
            name='isSpecial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student_user',
            name='photo',
            field=models.FileField(default=b'default.jpg', upload_to=b'photo'),
        ),
        migrations.AlterField(
            model_name='admin_user',
            name='college',
            field=models.CharField(default=b'all', max_length=50),
        ),
    ]
