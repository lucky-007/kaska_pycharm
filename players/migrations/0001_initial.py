# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(verbose_name='Email', error_messages={'unique': "We've have already this email"}, unique=True, max_length=255)),
                ('surname', models.CharField(verbose_name='Last name', max_length=25)),
                ('name', models.CharField(verbose_name='First name', max_length=15)),
                ('sex', models.CharField(verbose_name='Sex', default='m', choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('university', models.CharField(verbose_name='University', max_length=50)),
                ('phone', models.CharField(verbose_name='Phone', null=True, max_length=13)),
                ('experience', models.CharField(verbose_name='Experience', default='0-1', choices=[('0-1', 'less than 1 year'), ('1-2', '1-2 years'), ('2-3', '2-3 years'), ('3-5', '3-5 years'), ('>5', 'more than 5 years')], max_length=3)),
                ('position', models.CharField(verbose_name='Favourite position', default='han', choices=[('han', 'Handler'), ('mid', 'Middle'), ('lon', 'Long'), ('sid', 'On sideline')], max_length=3)),
                ('fav_throw', models.CharField(verbose_name='Favourite throw', default='for', choices=[('for', 'Forehand'), ('bac', 'Backhand'), ('bla', 'Blade'), ('ham', 'Hammer'), ('sco', 'Scoober'), ('ove', 'Overhand'), ('pus', 'Push-pass')], max_length=3)),
                ('style', models.CharField(verbose_name='Play style', default='uncon', choices=[('uncon', 'Uncontrollable'), ('slow', 'SlowPock'), ('cheek', 'Cheeky'), ('drunk', 'Drunk'), ('banan', 'Banana-cut')], max_length=5)),
                ('size', models.CharField(verbose_name='T-shirt size', default='xs', choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], max_length=2)),
                ('stud_photo', models.ImageField(verbose_name='Student ID (photo)', upload_to='', help_text='You can load the photo of the student ID later. For admins only', blank=True)),
                ('vk_id', models.CharField(null=True, unique=True, max_length=20)),
                ('access_token', models.CharField(null=True, max_length=100)),
                ('pool', models.SmallIntegerField(default=0)),
                ('photo', models.URLField(default='', null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', related_name='user_set', verbose_name='groups', related_query_name='user', blank=True)),
                ('team', models.ForeignKey(to='teams.Team', null=True, default=None, blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', related_name='user_set', verbose_name='user permissions', related_query_name='user', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
