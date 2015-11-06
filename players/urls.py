from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'^$', views.roster, name='roster'),
    url(r'(?P<player_id>[0-9]+)/$', views.player_info, name='info'),
    url(r'^change/$', views.player_change, name='change'),
    url(r'^create/$', views.player_create, name='create'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change/password/$', views.password_change, name='password_change'),
]