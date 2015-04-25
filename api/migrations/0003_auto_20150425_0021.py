# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150425_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drugsandsnp',
            name='pair',
        ),
        migrations.AddField(
            model_name='drugsandsnp',
            name='pairs',
            field=models.CharField(default='aaa', max_length=30),
            preserve_default=False,
        ),
    ]
