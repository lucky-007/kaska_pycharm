"""kaska_pycharm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import re

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import players.views

urlpatterns = [
    url(r'^$', players.views.index, name='index'),
    url(r'^gallery/$', players.views.gallery, name='gallery'),
    url(r'^tourn/$', players.views.tournament, name='tournament'),
    url(r'^teams/$', players.views.teams, name='teams'),
    url(r'^info/$', players.views.info, name='info'),
    url(r'^players/', include('players.urls', namespace='players')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        players.views.media, kwargs={'document_root': settings.MEDIA_ROOT}),
]
