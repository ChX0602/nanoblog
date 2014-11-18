# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0021_auto_20141025_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 25, 19, 26, 51, 458000), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=b'/static/img/default_user.png', upload_to=b'profile-photos', blank=True),
        ),
    ]
