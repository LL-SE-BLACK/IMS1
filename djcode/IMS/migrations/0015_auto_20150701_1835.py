# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0014_auto_20150701_1834'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pre_requisites',
        ),
        migrations.DeleteModel(
            name='Sys_log',
        ),
        migrations.AlterModelOptions(
            name='admin_user',
            options={'permissions': (('manage', 'Can manage admin user info'),)},
        ),
        migrations.AlterModelOptions(
            name='course_info',
            options={'permissions': (('manage', 'Can manage basic course info'),)},
        ),
        migrations.AlterModelOptions(
            name='faculty_user',
            options={'permissions': (('manage', 'Can manage faculty user info'),)},
        ),
    ]
