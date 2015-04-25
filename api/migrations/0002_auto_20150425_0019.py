# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugsandsnp',
            name='allele',
            field=models.CharField(default='hh', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugsandsnp',
            name='pair',
            field=models.CharField(default='hh', max_length=2),
            preserve_default=False,
        ),
    ]
