# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0013_auto_20150701_1831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student_user',
            options={'permissions': (('manage', 'Can manage stu user info'),)},
        ),
    ]
