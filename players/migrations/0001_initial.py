# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(max_length=255, error_messages={'unique': "We've have already this email"}, verbose_name='Email', unique=True)),
                ('surname', models.CharField(max_length=25, verbose_name='Last name')),
                ('name', models.CharField(max_length=15, verbose_name='First name')),
                ('university', models.CharField(max_length=15, verbose_name='University')),
                ('experience', models.PositiveSmallIntegerField(default=0, verbose_name='Experience')),
                ('position', models.CharField(max_length=3, choices=[('han', 'Handler'), ('mid', 'Middle'), ('lon', 'Long'), ('sid', 'On sideline')], verbose_name='Favourite position')),
                ('fav_throw', models.CharField(max_length=15, verbose_name='Favourite throw')),
                ('style', models.CharField(max_length=5, choices=[('slow', 'SlowPock'), ('regul', 'Regular'), ('cheek', 'Cheeky'), ('uncon', 'Uncontrollable'), ('drunk', 'Drunk')], verbose_name='Play style')),
                ('size', models.CharField(max_length=2, choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], verbose_name='T-shirt size')),
                ('stud_photo', models.ImageField(upload_to='', verbose_name='Student ID (photo)', help_text='You can load the photo of the student ID later. For admins only', blank=True)),
                ('vk_id', models.CharField(max_length=20, unique=True)),
                ('access_token', models.CharField(max_length=100)),
                ('pool', models.SmallIntegerField(default=0)),
                ('photo', models.URLField(default='', null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
