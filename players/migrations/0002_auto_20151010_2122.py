# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='vk_link',
            field=models.URLField(default='http://vk.com/', error_messages={'unique': "We've have already this"}, unique=True),
        ),
    ]
