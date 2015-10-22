from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'^$', views.roster, name='roster'),
    url(r'(?P<player_id>[0-9]+)/$', views.player_info, name='info'),
    url(r'(?P<player_id>[0-9]+)/change/$', views.player_change, name='change')
]