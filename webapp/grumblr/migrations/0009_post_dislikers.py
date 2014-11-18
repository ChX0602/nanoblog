# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0008_auto_20141003_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikers',
            field=models.ManyToManyField(to='grumblr.Profile'),
            preserve_default=True,
        ),
    ]
