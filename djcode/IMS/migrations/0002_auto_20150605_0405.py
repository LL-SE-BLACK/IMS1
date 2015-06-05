# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='class_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.RenameField(
            model_name='course_info',
            old_name='id',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='pre_requisites',
            old_name='courseid',
            new_name='course_id',
        ),
        migrations.RemoveField(
            model_name='class_info',
            name='courseid',
        ),
        migrations.AddField(
            model_name='class_info',
            name='class_id',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class_info',
            name='course_id',
            field=models.ForeignKey(default=0, to='IMS.Course_info'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course_info',
            name='college',
            field=models.CharField(default='Default College', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class_table',
            name='class_id',
            field=models.ForeignKey(to='IMS.Class_info'),
        ),
        migrations.AddField(
            model_name='class_table',
            name='student_id',
            field=models.ForeignKey(to='IMS.Student_user'),
        ),
    ]
