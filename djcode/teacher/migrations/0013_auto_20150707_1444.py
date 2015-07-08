# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_remove_history_h'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myauth',
            name='id',
        ),
        migrations.AlterField(
            model_name='myauth',
            name='UserId',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
    ]
