# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0010_auto_20150630_1018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin_user',
            options={'permissions': ('manage', 'Can manage faculties, students or courses')},
        ),
        migrations.AlterModelOptions(
            name='faculty_user',
            options={'permissions': ('manage', 'Can manage faculties, students or courses')},
        ),
        migrations.AlterModelOptions(
            name='student_user',
            options={'permissions': ('manage', 'Can manage faculties, students or courses')},
        ),
    ]
