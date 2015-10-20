

__author__ = 'filletofish'

from django.conf.urls import include, url
from django.contrib import admin
from vkPosts import views


urlpatterns = [
    # ex: /vk_posts/
    url(r'^$', views.index, name='index'),
]