# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_auto_20140919_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='city',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='info',
            name='country',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='info',
            name='dateofbirth',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='info',
            name='state',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='info',
            name='firstname',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='info',
            name='lastname',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='info',
            name='organization',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='info',
            name='user',
            field=models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL),
        ),
    ]
