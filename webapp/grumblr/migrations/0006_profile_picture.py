# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=datetime.date(2014, 10, 3), upload_to=b'profile-photos', blank=True),
            preserve_default=False,
        ),
    ]
