# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_player_stud_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='pool',
            field=models.SmallIntegerField(default=0),
        ),
    ]
