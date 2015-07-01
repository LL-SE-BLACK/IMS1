# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0011_auto_20150701_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin_user',
            options={},
        ),
        migrations.AlterModelOptions(
            name='faculty_user',
            options={},
        ),
        migrations.AlterModelOptions(
            name='student_user',
            options={},
        ),
    ]
