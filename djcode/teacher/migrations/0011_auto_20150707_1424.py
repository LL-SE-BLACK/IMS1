# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0010_history_h'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UserId', models.CharField(max_length=20, null=True)),
                ('OnAuthClassId', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='OnAuth',
        ),
    ]
