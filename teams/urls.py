__author__ = 'filletofish'

from django.conf.urls import include, url
from django.contrib import admin


from teams import views

# TODO: teams/ - displays all teams with players inside

urlpatterns = [
    # ex: /teams/select
    url(r'^select$', views.team_selection, name='index'),
]