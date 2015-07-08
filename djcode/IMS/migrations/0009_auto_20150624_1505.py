# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import IMS.models


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0008_auto_20150624_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_user',
            name='photo',
            field=models.FileField(default=b'photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
        migrations.AlterField(
            model_name='faculty_user',
            name='photo',
            field=models.FileField(default=b'photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
        migrations.AlterField(
            model_name='student_user',
            name='photo',
            field=models.FileField(default=b'photo/default.jpg', upload_to=IMS.models.get_photo_file_name),
        ),
    ]
